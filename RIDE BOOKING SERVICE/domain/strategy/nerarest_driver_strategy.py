


import math
from typing import List

from domain.driver import Driver
from domain.location import Location
from domain.strategy.driver_matching_strategy import DriverMatchingStrategy


class NearestDriverStrategy(DriverMatchingStrategy):
    def _distance_km(self, a: Location, b: Location) -> float:
        if a is None or b is None:
            return float('inf')
        lat_diff = a.latitude - b.latitude
        lon_diff = a.longitude - b.longitude
        # TODO: Replace with haversine for better accuracy.
        return math.sqrt(lat_diff ** 2 + lon_diff ** 2) * 111.0
        #distance_in_degrees * 111 ≈ distance_in_km   as : 1 degree of latitude ≈ 111 kilometers on Earth

    def find_matching_drivers(self, pickup: Location,candidates: List[Driver], max_results: int) -> List[Driver]:
        def sort_key(driver: Driver) -> float:
            return self._distance_km(pickup, driver.current_location) \
                if driver.current_location else float('inf')

        sorted_drivers = sorted(candidates, key=sort_key)
        return sorted_drivers[:max_results]