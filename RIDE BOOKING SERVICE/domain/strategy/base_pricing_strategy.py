


from domain.location import Location
from domain.strategy.pricing_strategy import PricingStrategy


class BasePricingStrategy(PricingStrategy):
    BASE_FARE_MINOR = 2000    # 20.00 in minor units
    PER_KM_MINOR = 800        # 8.00 per km
    PER_MINUTE_MINOR = 200    # 2.00 per minute

    def calculate_fare(self, pickup: Location, dropoff: Location, distance_km: float, duration_sec: int) -> int:
        distance_component = int(distance_km * self.PER_KM_MINOR)
        time_component = (duration_sec // 60) * self.PER_MINUTE_MINOR
        return max(self.BASE_FARE_MINOR, self.BASE_FARE_MINOR + distance_component + time_component)