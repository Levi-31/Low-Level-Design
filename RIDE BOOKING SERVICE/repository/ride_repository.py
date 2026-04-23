

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.ride import Ride
from domain.ride_status import RideStatus


class RideRepository(ABC):
    @abstractmethod
    def find_by_id(self, ride_id: str) -> Optional[Ride]:
        pass

    @abstractmethod
    def save(self, ride: Ride) -> None:
        pass

    @abstractmethod
    def find_by_rider_id(self, rider_id: str) -> List[Ride]:
        pass

    @abstractmethod
    def find_by_driver_id(self, driver_id: str) -> List[Ride]:
        pass

    @abstractmethod
    def find_by_status(self, status: RideStatus) -> List[Ride]:
        pass