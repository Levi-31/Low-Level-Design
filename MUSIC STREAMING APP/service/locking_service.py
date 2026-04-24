

import threading
from typing import Dict


class LockingService:
    def __init__(self):
        self.locks: Dict[str, bool] = {}
        self.mtx = threading.Lock()

    def acquire(self, key: str, timeout_ms: int) -> bool:
        with self.mtx:
            if key in self.locks:
                return False
            self.locks[key] = True
            return True

    def release(self, key: str) -> None:
        with self.mtx:
            self.locks.pop(key, None)