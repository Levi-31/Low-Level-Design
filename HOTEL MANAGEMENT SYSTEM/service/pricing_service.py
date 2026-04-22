


from typing import List

from domain.date_range import DateRange
from domain.nightly_price import NightlyPrice
from repository.room_type_repository import RoomTypeRepository
from repository.seasonal_price_repository import SeasonalPriceRepository


class PricingService:
    def __init__(self, room_type_repo: RoomTypeRepository, seasonal_price_repo: SeasonalPriceRepository):
        self.room_type_repo = room_type_repo
        self.seasonal_price_repo = seasonal_price_repo


    def rate_stay(self, hotel_id: str, room_type_id: str, date_range: DateRange) -> List[NightlyPrice]:
        room_type = self.room_type_repo.find_by_id(room_type_id)
        if not room_type:
            return []
        
        base_price = room_type.base_price
        nightly_prices = []

        for date_utc in range(date_range.check_in_date_utc, date_range.check_out_date_utc, 86400000):
            seasonal_price = self.seasonal_price_repo.find_by_key(hotel_id, room_type_id, date_utc)
            price = seasonal_price.price_minor if seasonal_price else base_price
            nightly_prices.append(NightlyPrice(date_utc, price))
        
        return nightly_prices
    
    def compute_total(self, nightly_prices: List[NightlyPrice]) -> int:
        return sum(np.price_minor for np in nightly_prices)

    def compute_average_price_per_night(self, nightly_prices: List[NightlyPrice], number_of_nights: int) -> float:
        if number_of_nights == 0:
            return 0.0
        return self.compute_total(nightly_prices) / number_of_nights