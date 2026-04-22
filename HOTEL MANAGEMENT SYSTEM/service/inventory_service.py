





import math
import time

from domain.date_range import DateRange
from repository.booking_repository import BookingRepository
from repository.hotel_repository import HotelRepository
from repository.room_type_repository import RoomTypeRepository


class InventoryService:
    def __init__(self, booking_repo: BookingRepository, hotel_repo: HotelRepository, room_type_repo: RoomTypeRepository):
        self.booking_repo = booking_repo
        self.hotel_repo = hotel_repo
        self.room_type_repo = room_type_repo

    def get_confirmed_bookings_count(self, hotel_id: str, room_type_id: str, date_utc: int) -> int:
        return self.booking_repo.count_confirmed_bookings(hotel_id, room_type_id, date_utc)

    def get_held_bookings_count(self, hotel_id: str, room_type_id: str, date_utc: int) -> int:
        now_utc = int(time.time() * 1000)
        return self.booking_repo.count_held_bookings(hotel_id, room_type_id, date_utc, now_utc)

    def get_checked_in_bookings_count(self, hotel_id: str, room_type_id: str, date_utc: int) -> int:
        return self.booking_repo.count_checked_in_bookings(hotel_id, room_type_id, date_utc)

    def check_availability(self, hotel_id: str, room_type_id: str, date_range: DateRange, qty: int) -> bool:
        room_type = self.room_type_repo.find_by_id(room_type_id)
        if not room_type:
            return False
        
        hotel = self.hotel_repo.find_by_id(hotel_id)
        if not hotel:
            return False

        total_rooms = room_type.total_rooms
        overbook_percent = hotel.default_overbook_percent
        overbook_allowed = math.ceil(total_rooms * overbook_percent / 100.0)

        for date_utc in range(date_range.check_in_date_utc, date_range.check_out_date_utc, 86400000):
            confirmed = self.get_confirmed_bookings_count(hotel_id, room_type_id, date_utc)
            held = self.get_held_bookings_count(hotel_id, room_type_id, date_utc)
            checked_in = self.get_checked_in_bookings_count(hotel_id, room_type_id, date_utc)

            available = total_rooms + overbook_allowed - confirmed - held - checked_in
            if available < qty:
                return False
        return True
