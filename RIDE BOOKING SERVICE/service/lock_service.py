


import threading


class LockService:
    """Simulated distributed lock service using threading locks.

    TODO: Replace with a real distributed lock (Redis/Memcached) for multi-node deployment.
    """

    def __init__(self):
        self._locks: dict = {}
        self._meta_lock = threading.Lock()

    def acquire(self, key: str, timeout_ms: int = 500) -> bool:
        with self._meta_lock:
            if key not in self._locks:
                self._locks[key] = threading.Lock()
            lock = self._locks[key]

        timeout_sec = timeout_ms / 1000.0
        acquired = lock.acquire(blocking=True, timeout=timeout_sec)
        return acquired

    def release(self, key: str) -> None:
        with self._meta_lock:
            lock = self._locks.get(key)
        if lock:
            try:
                lock.release()
            except RuntimeError:
                pass  # Already released
