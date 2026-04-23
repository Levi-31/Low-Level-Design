


from typing import Optional

from domain.location import Location
from domain.ride_status import RideStatus


class RideStatusResponse:
    def __init__(self, ride_id: str, status: RideStatus, driver_id: Optional[str],driver_name: Optional[str], driver_location: Optional[Location],estimated_fare: int, updated_at: int):
        self.ride_id = ride_id
        self.status = status
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.driver_location = driver_location
        self.estimated_fare = estimated_fare
        self.updated_at = updated_at