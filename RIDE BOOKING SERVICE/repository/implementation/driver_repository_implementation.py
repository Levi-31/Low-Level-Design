



import copy
import threading
from typing import List, Optional

from domain.driver import Driver
from domain.driver_status import DriverStatus
from repository.driver_repository import DriverRepository


class InMemoryDriverRepository(DriverRepository):
    def __init__(self):
        self._storage: dict[str,Driver] = {}
        self._lock = threading.Lock()

    def find_by_id(self, driver_id: str) -> Optional[Driver]:
        with self._lock:
            driver = self._storage.get(driver_id)
            return copy.copy(driver) if driver else None

    def save(self, driver: Driver) -> None:
        with self._lock:
            self._storage[driver.id] = copy.copy(driver)

    def find_by_status(self, status: DriverStatus) -> List[Driver]:
        with self._lock:
            return [copy.copy(d) for d in self._storage.values() if d.status == status]