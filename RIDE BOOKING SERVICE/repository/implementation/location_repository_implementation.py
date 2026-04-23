


import copy
import threading
from typing import Optional

from domain.location import Location
from repository.location_repository import LocationRepository


class InMemoryLocationRepository(LocationRepository):
    def __init__(self):
        self._storage: dict[str, Location] = {}
        self._lock = threading.Lock()

    def save_location(self, driver_id: str, location: Location) -> None:
        with self._lock:
            self._storage[driver_id] = copy.copy(location)

    def get_latest_location(self, driver_id: str) -> Optional[Location]:
        with self._lock:
            loc = self._storage.get(driver_id)
            return copy.copy(loc) if loc else None