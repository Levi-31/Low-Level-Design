


from dataclasses import dataclass
from typing import List
from domain.nightly_price import NightlyPrice


# RESPONSE DTO
@dataclass
class RoomTypeAvailability:
    room_type_id: str
    room_type_name: str
    capacity: int
    bed_type: str
    amenities: List[str]
    is_available: bool
    total_price: int
    avg_price_per_night: float
    nightly_prices: List[NightlyPrice]
