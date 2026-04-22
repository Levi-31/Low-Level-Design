

from abc import ABC, abstractmethod
from typing import List
from domain.room import Room

class RoomRepository(ABC):
    @abstractmethod
    def save(self, room: Room) -> Room:
        pass

    @abstractmethod
    def find_by_hotel_and_type(self, hotel_id: str, room_type_id: str) -> List[Room]:
        pass
