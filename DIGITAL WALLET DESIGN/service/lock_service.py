



import threading
import time


class LockService:
    """
    Per-key mutual exclusion using threading.Lock.
    TODO: Replace with a distributed lock (e.g., Redis SET NX EX) for multi-node deployments.
    """

    def __init__(self):
        self._lock_map: dict = {}
        self._map_lock = threading.Lock()

    def _get_or_create_lock(self, key: str) -> threading.Lock:
        with self._map_lock:
            if key not in self._lock_map:
                self._lock_map[key] = threading.Lock()
            return self._lock_map[key]
        
    def acquire(self, key: str, timeout_ms: int) -> bool:
        """Acquire the lock for key within timeout_ms milliseconds."""
        lock = self._get_or_create_lock(key)
        deadline = time.time() + timeout_ms / 1000.0
        while time.time() < deadline:
            if lock.acquire(blocking=False):
                return True
            time.sleep(0.005)
        return False
    
    def release(self, key: str):
        with self._map_lock:
            lock = self._lock_map.get(key)
        if lock is not None:
            try:
                lock.release()
            except RuntimeError:
                pass  # Already released