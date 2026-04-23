

from abc import ABC, abstractmethod

from domain.location import Location


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fare(self, pickup: Location, dropoff: Location,distance_km: float, duration_sec: int) -> int:
        pass