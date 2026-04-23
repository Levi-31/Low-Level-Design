

from domain.fare_estimate_response import FareEstimateResponse
from domain.location import Location
from domain.strategy.pricing_strategy import PricingStrategy


class PricingService:
    def __init__(self, pricing_strategy: PricingStrategy):
        self._pricing_strategy = pricing_strategy

    def estimate_fare(self, pickup: Location, dropoff: Location,distance_km: float, duration_sec: int) -> FareEstimateResponse:
        fare_minor = self._pricing_strategy.calculate_fare(pickup, dropoff, distance_km, duration_sec)
        return FareEstimateResponse(fare_minor, distance_km, duration_sec, "USD")