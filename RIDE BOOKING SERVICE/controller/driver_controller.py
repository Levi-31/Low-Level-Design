


from domain.location import Location
from service.driver_service import DriverService
from service.ride_service import RideService


class DriverController:
    def __init__(self, driver_service: DriverService, ride_service: RideService):
        self._driver_service = driver_service
        self._ride_service = ride_service

    def go_online(self, driver_id: str) -> None:
        self._driver_service.go_online(driver_id)

    def go_offline(self, driver_id: str) -> None:
        self._driver_service.go_offline(driver_id)

    def update_location(self, driver_id: str, location: Location) -> None:
        self._driver_service.update_location(driver_id, location)

    def accept_ride(self, ride_id: str, driver_id: str) -> None:
        self._ride_service.driver_accept(ride_id, driver_id)

    def decline_ride(self, ride_id: str, driver_id: str) -> None:
        self._ride_service.driver_decline(ride_id, driver_id)

    def start_ride(self, ride_id: str, driver_id: str) -> None:
        self._ride_service.start_ride(ride_id, driver_id)

    def complete_ride(self, ride_id: str, driver_id: str) -> None:
        self._ride_service.complete_ride(ride_id, driver_id)