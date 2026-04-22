from typing import Optional, Dict
from domain.seasonal_price import SeasonalPrice
from repository.seasonal_price_repository import SeasonalPriceRepository


class SeasonalPriceRepositoryImpl(SeasonalPriceRepository):
    def __init__(self):
        self.prices: Dict[str, SeasonalPrice] = {}

    def _build_key(self, hotel_id: str, room_type_id: str, date_utc: int) -> str:
        return f"{hotel_id}:{room_type_id}:{date_utc}"

    def upsert(self, price: SeasonalPrice) -> SeasonalPrice:
        key = self._build_key(price.hotel_id, price.room_type_id, price.date_utc)
        self.prices[key] = price
        return price

    def find_by_key(self, hotel_id: str, room_type_id: str, date_utc: int) -> Optional[SeasonalPrice]:
        key = self._build_key(hotel_id, room_type_id, date_utc)
        return self.prices.get(key)
