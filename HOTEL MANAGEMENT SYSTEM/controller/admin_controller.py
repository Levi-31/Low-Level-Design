



import time
import uuid

from domain.booking import Booking
from domain.cancellation_policy import CancellationPolicy
from domain.hotel import Hotel
from domain.room_type import RoomType
from domain.seasonal_price import SeasonalPrice
from repository.cancellation_policy_repository import CancellationPolicyRepository
from repository.hotel_repository import HotelRepository
from repository.room_repository import RoomRepository
from repository.room_type_repository import RoomTypeRepository
from repository.seasonal_price_repository import SeasonalPriceRepository
from service.booking_service import BookingService


class AdminController:
    def __init__(self, hotel_repo: HotelRepository, room_type_repo: RoomTypeRepository,
                 room_repo: RoomRepository, seasonal_price_repo: SeasonalPriceRepository,
                 cancellation_policy_repo: CancellationPolicyRepository, 
                 booking_ser: BookingService):
        self.hotel_repo = hotel_repo
        self.room_type_repo = room_type_repo
        self.room_repo = room_repo
        self.seasonal_price_repo = seasonal_price_repo
        self.cancellation_policy_repo = cancellation_policy_repo
        self.booking_ser = booking_ser

    def create_or_update_hotel(self, hotel: Hotel) -> Hotel:
        return self.hotel_repo.save(hotel)

    def create_or_update_room_type(self, room_type: RoomType) -> RoomType:
        return self.room_type_repo.save(room_type)

    def update_overbooking_percent(self, hotel_id: str, percent: int):
        hotel = self.hotel_repo.find_by_id(hotel_id)
        if hotel:
            hotel.default_overbook_percent = percent
            self.hotel_repo.save(hotel)

    def set_seasonal_price(self, hotel_id: str, room_type_id: str, date_utc: int, price_minor: int) -> SeasonalPrice:
        existing = self.seasonal_price_repo.find_by_key(hotel_id, room_type_id, date_utc)
        if existing:
            existing.price_minor = price_minor
            price = existing
        else:
            now = int(time.time() * 1000)
            price = SeasonalPrice(
                id=str(uuid.uuid4()),
                hotel_id=hotel_id,
                room_type_id=room_type_id,
                date_utc=date_utc,
                price_minor=price_minor,
                created_at=now
            )
        return self.seasonal_price_repo.upsert(price)

    def create_or_update_policy(self, policy: CancellationPolicy) -> CancellationPolicy:
        return self.cancellation_policy_repo.save(policy)

    def check_in(self, booking_id: str, room_id: str, check_in_time_utc: int) -> Booking:
        return self.booking_ser.check_in(booking_id, room_id, check_in_time_utc)

    def check_out(self, booking_id: str, check_out_time_utc: int) -> Booking:
        return self.booking_ser.check_out(booking_id, check_out_time_utc)
