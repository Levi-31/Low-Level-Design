

from typing import List

from domain.booking import Booking
from service.user_service import UserService


class DashboardController:
    def __init__(self, user_ser: UserService):
        self.user_ser = user_ser

    def list_user_bookings(self, user_id: str) -> List[Booking]:
        return self.user_ser.list_user_bookings(user_id)