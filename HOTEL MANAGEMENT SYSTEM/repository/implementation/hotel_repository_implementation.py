from typing import List, Optional, Dict
from domain.hotel import Hotel
from repository.hotel_repository import HotelRepository


class HotelRepositoryImpl(HotelRepository):
    def __init__(self):
        self.hotels: Dict[str, Hotel] = {} # id --> instance

    def save(self, hotel: Hotel) -> Hotel:
        self.hotels[hotel.id] = hotel
        return hotel

    def find_by_id(self, hotel_id: str) -> Optional[Hotel]:
        return self.hotels.get(hotel_id)

    def find_by_location(self, city: str, country: str) -> List[Hotel]:
        return [h for h in self.hotels.values() 
                if h.city == city and h.country == country and h.is_active]