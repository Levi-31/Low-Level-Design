

from abc import ABC, abstractmethod
from typing import Optional

from domain.location import Location


class LocationRepository(ABC):
    @abstractmethod
    def save_location(self, driver_id: str, location: Location) -> None:
        pass

    @abstractmethod
    def get_latest_location(self, driver_id: str) -> Optional[Location]:
        pass