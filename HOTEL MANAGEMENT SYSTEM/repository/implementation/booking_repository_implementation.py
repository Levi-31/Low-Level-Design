

from typing import List, Optional, Dict
from domain.booking import Booking
from domain.booking_status import BookingStatus
from ..booking_repository import BookingRepository

class BookingRepositoryImpl(BookingRepository):
    def __init__(self):
        self.bookings: Dict[str, Booking] = {}

    def save(self, booking: Booking) -> Booking:
        self.bookings[booking.id] = booking
        return booking

    def find_by_id(self, booking_id: str) -> Optional[Booking]:
        return self.bookings.get(booking_id)

    def find_by_user(self, user_id: str) -> List[Booking]:
        return [b for b in self.bookings.values() if b.user_id == user_id]

    def count_confirmed_bookings(self, hotel_id: str, room_type_id: str, date_utc: int) -> int:
        return sum(1 for b in self.bookings.values() 
                  if b.hotel_id == hotel_id and 
                  b.room_type_id == room_type_id and 
                  b.booking_status == BookingStatus.CONFIRMED and 
                  b.check_in_date_utc <= date_utc < b.check_out_date_utc)

    def count_held_bookings(self, hotel_id: str, room_type_id: str, date_utc: int, now_utc: int) -> int:
        return sum(1 for b in self.bookings.values() 
                  if b.hotel_id == hotel_id and 
                  b.room_type_id == room_type_id and 
                  b.booking_status == BookingStatus.HELD and 
                  b.check_in_date_utc <= date_utc < b.check_out_date_utc and 
                  b.hold_expires_at > now_utc)

    def count_checked_in_bookings(self, hotel_id: str, room_type_id: str, date_utc: int) -> int:
        return sum(1 for b in self.bookings.values() 
                  if b.hotel_id == hotel_id and 
                  b.room_type_id == room_type_id and 
                  b.booking_status == BookingStatus.CHECKED_IN and 
                  b.check_in_date_utc <= date_utc < b.check_out_date_utc)
