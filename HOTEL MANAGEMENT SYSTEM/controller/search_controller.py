

from typing import List

from domain.date_range import DateRange
from domain.hotel import Hotel
from domain.room_type_availability import RoomTypeAvailability
from domain.search_filter import SearchFilter
from service.search_service import SearchService


class SearchController:
    def __init__(self, search_ser: SearchService):
        self.search_ser = search_ser

    def search_hotels(self, search_filter: SearchFilter) -> List[Hotel]:
        return self.search_ser.search_hotels(search_filter)

    def get_availability(self, hotel_id: str, date_range: DateRange) -> List[RoomTypeAvailability]:
        return self.search_ser.get_availability(hotel_id, date_range)
    
