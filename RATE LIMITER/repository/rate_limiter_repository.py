


import threading
from typing import Any, Dict


class RateLimiterRepository:
    def __init__(self):
        self.lock = threading.Lock()
        self._storage: Dict[Any, Any] = {}

    def get_state(self, key: Any, default: Any = None) -> Any:
        return self._storage.get(key, default)

    def set_state(self, key: Any, value: Any) -> None:
        self._storage[key] = value

    def delete_state(self, key: Any) -> None:
        if key in self._storage:
            del self._storage[key]
        
