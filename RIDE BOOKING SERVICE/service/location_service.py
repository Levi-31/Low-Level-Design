

import math

from typing import Optional

from domain.location import Location
from repository.location_repository import LocationRepository


class LocationService:
    def __init__(self, location_repository: LocationRepository):
        self._location_repository = location_repository

    def update_driver_location(self, driver_id: str, location: Location) -> None:
        self._location_repository.save_location(driver_id, location)

    def get_driver_location(self, driver_id: str) -> Optional[Location]:
        return self._location_repository.get_latest_location(driver_id)

    def calculate_distance_km(self, from_loc: Location, to_loc: Location) -> float:
        if from_loc is None or to_loc is None:
            return 0.0
        lat_diff = from_loc.latitude - to_loc.latitude
        lon_diff = from_loc.longitude - to_loc.longitude
        # TODO: Use map provider to calculate distance.
        return math.sqrt(lat_diff ** 2 + lon_diff ** 2) * 111.0

    def estimate_duration_sec(self, distance_km: float) -> int:
        avg_speed_kmh = 35.0  # simple assumption
        hours = distance_km / avg_speed_kmh
        return int(hours * 3600)