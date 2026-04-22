



from dataclasses import dataclass

@dataclass
class Hotel:
    id: str
    name: str
    address: str
    city: str
    country: str
    lat: float
    lng: float
    rating: float
    is_active: bool
    default_overbook_percent: int
    cancellation_policy_id: str
    created_at: int