



import copy
import threading
from typing import Optional , List

from domain.ride import Ride
from domain.ride_status import RideStatus
from repository.ride_repository import RideRepository


class InMemoryRideRepository(RideRepository):
    def __init__(self):
        self._storage: dict[str,Ride] = {}
        self._lock = threading.Lock()

    def find_by_id(self, ride_id: str) -> Optional[Ride]:
        with self._lock:
            ride = self._storage.get(ride_id)
            return copy.copy(ride) if ride else None

    def save(self, ride: Ride) -> None:
        with self._lock:
            self._storage[ride.id] = copy.copy(ride)

    def find_by_rider_id(self, rider_id: str) -> List[Ride]:
        with self._lock:
            return [copy.copy(r) for r in self._storage.values() if r.rider_id == rider_id]

    def find_by_driver_id(self, driver_id: str) -> List[Ride]:
        with self._lock:
            if not driver_id:
                return []
            return [copy.copy(r) for r in self._storage.values() if r.driver_id == driver_id]

    def find_by_status(self, status: RideStatus) -> List[Ride]:
        with self._lock:
            return [copy.copy(r) for r in self._storage.values() if r.status == status]
