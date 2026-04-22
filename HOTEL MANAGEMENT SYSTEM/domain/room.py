from dataclasses import dataclass

@dataclass
class Room:
    id: str
    hotel_id: str
    room_type_id: str
    room_number: str
    is_active: bool
    created_at: int