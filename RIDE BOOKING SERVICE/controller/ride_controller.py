


from domain.fare_estimate_response import FareEstimateResponse
from domain.location import Location
from domain.ride import Ride
from domain.ride_request import RideRequest
from domain.ride_status_response import RideStatusResponse
from service.ride_service import RideService


class RideController:
    def __init__(self, ride_service: RideService):
        self._ride_service = ride_service

    def get_fare_estimate(self, pickup: Location, dropoff: Location) -> FareEstimateResponse:
        return self._ride_service.estimate_fare(pickup, dropoff)

    def request_ride(self, request: RideRequest) -> Ride:
        return self._ride_service.request_ride(request)

    def get_ride_status(self, ride_id: str) -> RideStatusResponse:
        return self._ride_service.get_ride_status(ride_id)

    def cancel_ride(self, ride_id: str, reason: str) -> None:
        self._ride_service.cancel_ride(ride_id, reason)