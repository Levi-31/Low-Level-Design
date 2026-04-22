


from typing import List

from domain.booking import Booking
from repository.booking_repository import BookingRepository


class UserService:
    def __init__(self, booking_repo: BookingRepository):
        self.booking_repo = booking_repo

    def list_user_bookings(self, user_id: str) -> List[Booking]:
        return self.booking_repo.find_by_user(user_id)