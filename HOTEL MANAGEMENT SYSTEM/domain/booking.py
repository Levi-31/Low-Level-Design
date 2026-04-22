

from dataclasses import dataclass
from typing import List, Optional

from domain.booking_status import BookingStatus
from domain.nightly_price import NightlyPrice
from domain.transaction_status import TransactionStatus


@dataclass
class Booking:
    id: str
    user_id: str
    hotel_id: str
    room_type_id: str
    check_in_date_utc: int
    check_out_date_utc: int
    nightly_prices: List[NightlyPrice]
    total_amount_minor: int
    booking_status: BookingStatus
    payment_status: TransactionStatus
    allocated_room_id: Optional[str] = None
    check_in_time_utc: int = 0
    check_out_time_utc: int = 0
    hold_expires_at: int = 0
    created_at: int = 0