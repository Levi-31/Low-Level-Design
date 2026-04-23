
from typing import Optional

from domain.driver import Driver
from domain.driver_status import DriverStatus
from domain.location import Location
from repository.driver_repository import DriverRepository


class DriverService:
    def __init__(self, driver_repository: DriverRepository):
        self._driver_repository = driver_repository


    def go_online(self, driver_id: str) -> None:
        driver = self._driver_repository.find_by_id(driver_id)
        if not driver:
            raise ValueError(f"Driver not found: {driver_id}")
        driver.status = DriverStatus.ONLINE
        self._driver_repository.save(driver)

    def go_offline(self, driver_id: str) -> None:
        driver = self._driver_repository.find_by_id(driver_id)
        if not driver:
            raise ValueError(f"Driver not found: {driver_id}")
        driver.status = DriverStatus.OFFLINE
        self._driver_repository.save(driver)

    def update_location(self, driver_id: str, location: Location) -> None:
        driver = self._driver_repository.find_by_id(driver_id)
        if not driver:
            raise ValueError(f"Driver not found: {driver_id}")
        driver.current_location = location
        driver.last_location_update = location.timestamp
        self._driver_repository.save(driver)

    def find_by_id(self, driver_id: str) -> Optional[Driver]:
        return self._driver_repository.find_by_id(driver_id)