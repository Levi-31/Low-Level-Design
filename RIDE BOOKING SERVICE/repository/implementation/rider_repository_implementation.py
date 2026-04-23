


import copy
import threading
from typing import Dict, Optional
from domain.rider import Rider
from repository.rider_repository import RiderRepository


class InMemoryRiderRepository(RiderRepository):
    def __init__(self):
        self._storage: Dict[str , Rider] = {}
        self._lock = threading.Lock()

    def find_by_id(self, rider_id: str) -> Optional[Rider]:
        with self._lock:
            rider = self._storage.get(rider_id)
            return copy.copy(rider) if rider else None

    def save(self, rider: Rider) -> None:
        with self._lock:
            self._storage[rider.id] = copy.copy(rider)