


from domain.booking import Booking
from domain.date_range import DateRange
from service.booking_service import BookingService


class BookingController:
    def __init__(self, booking_ser: BookingService):
        self.booking_ser = booking_ser

    def create_booking(self, user_id: str, hotel_id: str, room_type_id: str, 
                       date_range: DateRange, expected_total_price: int) -> Booking:
        return self.booking_ser.create_booking(user_id, hotel_id, room_type_id, date_range, expected_total_price)

    def cancel_booking(self, booking_id: str, user_id: str):
        self.booking_ser.cancel_booking(booking_id, user_id)
