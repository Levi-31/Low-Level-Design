from abc import ABC, abstractmethod
from typing import List, Optional
from domain.room_type import RoomType

class RoomTypeRepository(ABC):
    @abstractmethod
    def save(self, room_type: RoomType) -> RoomType:
        pass

    @abstractmethod
    def find_by_id(self, room_type_id: str) -> Optional[RoomType]:
        pass

    @abstractmethod
    def find_by_hotel(self, hotel_id: str) -> List[RoomType]:
        pass