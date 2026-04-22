



import math
from typing import List

from domain.date_range import DateRange
from domain.hotel import Hotel
from domain.room_type_availability import RoomTypeAvailability
from domain.search_filter import SearchFilter
from repository.booking_repository import BookingRepository
from repository.hotel_repository import HotelRepository
from repository.room_repository import RoomRepository
from repository.room_type_repository import RoomTypeRepository
from service.inventory_service import InventoryService
from service.pricing_service import PricingService


class SearchService:
    def __init__(self, hotel_repo: HotelRepository, room_type_repo: RoomTypeRepository,
                 room_repo: RoomRepository, pricing_ser: PricingService,
                 booking_repo: BookingRepository):
        self.hotel_repo = hotel_repo
        self.room_type_repo = room_type_repo
        self.room_repo = room_repo
        self.pricing_ser = pricing_ser
        self.inventory_ser = InventoryService(booking_repo, hotel_repo, room_type_repo)


    def search_hotels(self, search_filter: SearchFilter) -> List[Hotel]:
        if search_filter.city and search_filter.country:
            return self.hotel_repo.find_by_location(search_filter.city, search_filter.country)
        return []

    def get_availability(self, hotel_id: str, date_range: DateRange) -> List[RoomTypeAvailability]:
        hotel = self.hotel_repo.find_by_id(hotel_id)
        if not hotel:
            return []

        room_types = self.room_type_repo.find_by_hotel(hotel_id)
        result = []

        overbook_percent = hotel.default_overbook_percent
        for rt in room_types:
            if not rt.is_active:
                continue

            room_type_id = rt.id
            total_rooms = rt.total_rooms
            overbook_allowed = math.ceil(total_rooms * overbook_percent / 100.0)

            available = True
            min_available = float('inf')
            for date_utc in range(date_range.check_in_date_utc, date_range.check_out_date_utc, 86400000):
                confirmed = self.inventory_ser.get_confirmed_bookings_count(hotel_id, room_type_id, date_utc)
                held = self.inventory_ser.get_held_bookings_count(hotel_id, room_type_id, date_utc)
                checked_in = self.inventory_ser.get_checked_in_bookings_count(hotel_id, room_type_id, date_utc)

                available_for_night = total_rooms + overbook_allowed - confirmed - held - checked_in
                min_available = min(min_available, available_for_night)
                if available_for_night < 1:
                    available = False
                    break

            if available and min_available >= 1:
                nightly_prices = self.pricing_ser.rate_stay(hotel_id, room_type_id, date_range)
                total_price = self.pricing_ser.compute_total(nightly_prices)
                num_nights = (date_range.check_out_date_utc - date_range.check_in_date_utc) // 86400000
                avg_price = self.pricing_ser.compute_average_price_per_night(nightly_prices, num_nights)

                result.append(RoomTypeAvailability(
                    room_type_id=rt.id,
                    room_type_name=rt.name,
                    capacity=rt.capacity,
                    bed_type=rt.bed_type,
                    amenities=rt.amenities,
                    is_available=True,
                    total_price=total_price,
                    avg_price_per_night=avg_price,
                    nightly_prices=nightly_prices
                ))
        
        return result