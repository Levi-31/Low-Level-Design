



from dataclasses import dataclass
from typing import Optional

# REQUEST DTO 

@dataclass
class SearchFilter:
    city: Optional[str] = None
    country: Optional[str] = None
    check_in_date_utc: Optional[int] = None
    check_out_date_utc: Optional[int] = None
    min_rating: Optional[float] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None