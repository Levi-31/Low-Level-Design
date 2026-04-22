


from abc import ABC, abstractmethod
from typing import Optional
from domain.seasonal_price import SeasonalPrice

class SeasonalPriceRepository(ABC):
    @abstractmethod
    def upsert(self, price: SeasonalPrice) -> SeasonalPrice:
        pass

    @abstractmethod
    def find_by_key(self, hotel_id: str, room_type_id: str, date_utc: int) -> Optional[SeasonalPrice]:
        pass