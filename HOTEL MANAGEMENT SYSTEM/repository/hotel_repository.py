

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.hotel import Hotel

class HotelRepository(ABC):
    @abstractmethod
    def save(self, hotel: Hotel) -> Hotel:
        pass

    @abstractmethod
    def find_by_id(self, hotel_id: str) -> Optional[Hotel]:
        pass

    @abstractmethod
    def find_by_location(self, city: str, country: str) -> List[Hotel]:
        pass