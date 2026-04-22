from dataclasses import dataclass
from typing import List

@dataclass
class RoomType:
    id: str
    hotel_id: str
    name: str
    capacity: int
    bed_type: str
    base_price: int
    amenities: List[str]
    total_rooms: int
    is_active: bool
    created_at: int