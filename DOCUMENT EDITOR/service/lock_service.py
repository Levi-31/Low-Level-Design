import threading

class LockService:
    def __init__(self):
        self._mutex = threading.Lock()

    def acquire_lock(self, blocking: bool = True) -> bool:
        """
        Acquires the lock. If blocking is False, returns False immediately if the lock is held.
        """
        acquired = self._mutex.acquire(blocking=blocking)
        if acquired:
            print("[LockService] Lock acquired.")
        return acquired

    def release_lock(self):
        try:
            self._mutex.release()
            print("[LockService] Lock released.")
        except RuntimeError:
            print("[LockService] Error: Attempted to release an unacquired lock.")
