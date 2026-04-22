

from typing import List, Dict
from domain.room import Room
from ..room_repository import RoomRepository

class RoomRepositoryImpl(RoomRepository):
    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def save(self, room: Room) -> Room:
        self.rooms[room.id] = room
        return room

    def find_by_hotel_and_type(self, hotel_id: str, room_type_id: str) -> List[Room]:
        return [r for r in self.rooms.values() 
                if r.hotel_id == hotel_id and r.room_type_id == room_type_id and r.is_active]
