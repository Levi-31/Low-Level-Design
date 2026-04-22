



from dataclasses import dataclass


@dataclass
class SeasonalPrice:
    id: str
    hotel_id: str
    room_type_id: str
    date_utc: int
    price_minor: int
    created_at: int