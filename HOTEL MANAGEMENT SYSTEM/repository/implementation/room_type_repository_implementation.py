

from typing import List, Optional, Dict
from domain.room_type import RoomType
from repository.room_type_repository import RoomTypeRepository


class RoomTypeRepositoryImpl(RoomTypeRepository):
    def __init__(self):
        self.room_types: Dict[str, RoomType] = {}

    def save(self, room_type: RoomType) -> RoomType:
        self.room_types[room_type.id] = room_type
        return room_type

    def find_by_id(self, room_type_id: str) -> Optional[RoomType]:
        return self.room_types.get(room_type_id)

    def find_by_hotel(self, hotel_id: str) -> List[RoomType]:
        return [rt for rt in self.room_types.values() 
                if rt.hotel_id == hotel_id and rt.is_active]
