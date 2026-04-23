# Lock Service Analysis and Redis Implementation Plan

## 1. Analysis of the Current `lock_service.py`

The current implementation of `lock_service.py` (`LockService` class) provides an in-memory, threading-based locking mechanism. This is critical for preventing race conditions in a concurrent environment, such as when two concurrent threads attempt to withdraw funds or transfer money from the exact same wallet simultaneously.

By assigning a specific lock to a key (usually the `wallet_id`), the system ensures that operations on a specific wallet are handled atomically without locking the entire system.

### In-Depth Method Explanations

#### `__init__(self)`
*   **Purpose**: Initializes the synchronization primitives required for managing locks dynamically.
*   **Details**: 
    *   `self._lock_map`: A dictionary used to map string keys (like `wallet_lock_<wallet_id>`) to their corresponding `threading.Lock()` instances.
    *   `self._map_lock`: A master thread lock (`threading.Lock()`). This lock is **not** used for business logic; rather, it's used to safely mutate or read the `_lock_map` itself to prevent dictionary corruption if multiple threads try to request new locks at the same microsecond.

#### `_get_or_create_lock(self, key: str) -> threading.Lock`
*   **Purpose**: Retrieves an existing lock for a given key, or creates a new one safely if it doesn't exist.
*   **Details**: 
    *   It uses `with self._map_lock:` to ensure only one thread can inspect or alter the `_lock_map` at any given time.
    *   If the provided `key` is missing, it provisions a new `threading.Lock()` and stores it in the map.
    *   It returns the lock instance assigned to that key. This method guarantees that for any specific key, the exact same lock object is returned to all competing threads.

#### `acquire(self, key: str, timeout_ms: int) -> bool`
*   **Purpose**: Attempts to gain exclusive access to the lock associated with the provided `key` within a specific timeframe.
*   **Details**: 
    *   First, it calls `_get_or_create_lock(key)` to get the specific target lock.
    *   It calculates a `deadline` (current time + timeout).
    *   **Polling Loop (Spin-Lock)**: Instead of blocking indefinitely, it attempts a non-blocking acquire: `lock.acquire(blocking=False)`.
    *   If it fails to acquire the lock immediately, it uses `time.sleep(0.005)` (sleeps for 5 milliseconds) and retries.
    *   This loop continues until the lock is acquired (returns `True`) or the deadline is breached (returns `False`). This polling approach prevents threads from hanging forever if a lock is orphaned or held too long.

#### `release(self, key: str)`
*   **Purpose**: Releases the exclusive access to the lock.
*   **Details**: 
    *   It safely queries `_lock_map` (using the master `_map_lock`) to find the lock object.
    *   If the lock exists, it attempts to call `.release()`.
    *   It traps a `RuntimeError`, which `threading.Lock` throws if a release is attempted on an already unlocked lock. This makes the release method idempotent and safe against double-releases or releasing expired locks.

---

## 2. Implementation Plan for Redis Setup

The current in-memory threading lock is perfect for single-node deployments but will fail in a distributed environment (e.g., Kubernetes with multiple replica pods), because threads in Pod A do not share memory with threads in Pod B. 

To make the system distributed, we will migrate `LockService` to use a Redis-based Distributed Lock.

### Prerequisites
*   A running Redis instance/cluster.
*   The `redis-py` library installed (`pip install redis`).

### Redis Locking Mechanism Strategy
We will use the **SET NX PX** strategy (Set if Not eXists, with Expiry).
*   **NX**: Ensures the key is only created if it doesn't already exist (acquiring the lock).
*   **PX**: Automatically expires the lock after a timeout to prevent deadlocks if a server crashes while holding a lock.
*   **Unique Token**: A unique UUID is saved as the value of the Redis key to ensure a node can only release the lock it specifically acquired.

### Proposed Code Implementation

```python
import time
import uuid
import redis

class RedisLockService:
    def __init__(self, redis_host='localhost', redis_port=6379, db=0):
        # Initialize Redis client connection pool
        self._redis = redis.Redis(host=redis_host, port=redis_port, db=db, decode_responses=True)
        # Thread-local storage to keep track of the unique tokens for each lock
        # mapping key -> token
        self._local_tokens = {}

    def acquire(self, key: str, timeout_ms: int) -> bool:
        """
        Acquire distributed lock via Redis.
        """
        token = str(uuid.uuid4())
        deadline = time.time() + (timeout_ms / 1000.0)
        
        # We set an automatic expiration on the lock slightly larger than our timeout 
        # to ensure it releases eventually if the process dies.
        lock_validity_ms = timeout_ms + 1000 
        
        while time.time() < deadline:
            # SET <key> <token> NX PX <validity>
            success = self._redis.set(key, token, nx=True, px=lock_validity_ms)
            if success:
                self._local_tokens[key] = token
                return True
            time.sleep(0.01) # Sleep 10ms before retrying
            
        return False

    def release(self, key: str):
        """
        Release the lock using a Lua script to ensure atomicity.
        Only the owner holding the correct token can release it.
        """
        token = self._local_tokens.get(key)
        if not token:
            return # We don't own this lock

        # Lua script ensures we only delete the key IF the value matches our token
        lua_script = \"\"\"
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        \"\"\"
        self._redis.eval(lua_script, 1, key, token)
        
        # Clean up local token reference
        del self._local_tokens[key]
```

### Integration Steps
1.  **Dependencies**: Add `redis` to `requirements.txt`.
2.  **Configuration**: Update application configuration to pass Redis connection strings to the Service container layer.
3.  **Swap Implementations**: In the main dependency injection setup (e.g., inside `main.py` or the container manager), replace the instantiation of `LockService()` with `RedisLockService(redis_client)`. Since the signature of `acquire` and `release` remains identical, `TransactionService` requires zero changes.
4.  **Testing**: Write integration tests spinning up a Testcontainers Redis instance, spawning multiple processes, and confirming that concurrent deposits/transfers to the same wallet result in correct final balances.
