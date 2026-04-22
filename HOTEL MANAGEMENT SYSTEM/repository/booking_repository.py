

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.booking import Booking

class BookingRepository(ABC):
    @abstractmethod
    def save(self, booking: Booking) -> Booking:
        pass

    @abstractmethod
    def find_by_id(self, booking_id: str) -> Optional[Booking]:
        pass

    @abstractmethod
    def find_by_user(self, user_id: str) -> List[Booking]:
        pass

    @abstractmethod
    def count_confirmed_bookings(self, hotel_id: str, room_type_id: str, date_utc: int) -> int:
        pass

    @abstractmethod
    def count_held_bookings(self, hotel_id: str, room_type_id: str, date_utc: int, now_utc: int) -> int:
        pass

    @abstractmethod
    def count_checked_in_bookings(self, hotel_id: str, room_type_id: str, date_utc: int) -> int:
        pass
