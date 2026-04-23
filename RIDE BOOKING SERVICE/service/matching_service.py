




import time
from typing import Optional

from domain.driver import Driver
from domain.driver_status import DriverStatus
from domain.notification_message import NotificationMessage
from domain.ride import Ride
from domain.ride_status import RideStatus
from domain.strategy.driver_matching_strategy import DriverMatchingStrategy
from repository.driver_repository import DriverRepository
from repository.ride_repository import RideRepository
from service.lock_service import LockService
from service.notification.notification_service import NotificationService



DEFAULT_MAX_RESULTS = 3
DRIVER_RESPONSE_TIMEOUT_SEC = 30

class MatchingService:
    def __init__(self, driver_repository: DriverRepository,
                 ride_repository: RideRepository,
                 matching_strategy: DriverMatchingStrategy,
                 lock_service: LockService,
                 notification_service: NotificationService):
        self._driver_repository = driver_repository
        self._ride_repository = ride_repository
        self._matching_strategy = matching_strategy
        self._lock_service = lock_service
        self._notification_service = notification_service

    def match_driver(self, ride: Ride) -> Optional[Driver]:
        if ride.status != RideStatus.REQUESTED:
            return None

        available_drivers = self._driver_repository.find_by_status(DriverStatus.ONLINE)
        suggestions = self._matching_strategy.find_matching_drivers(
            ride.pickup_location, available_drivers, DEFAULT_MAX_RESULTS)

        if not suggestions:
            return None

        for driver in suggestions:
            lock_key = f"driver_lock_{driver.id}"
            acquired = self._lock_service.acquire(lock_key, 200)
            if not acquired:
                continue

            try:
                latest_driver = self._driver_repository.find_by_id(driver.id) or driver
                if latest_driver.status != DriverStatus.ONLINE:
                    continue

                self._notification_service.send(NotificationMessage(
                    latest_driver.id,
                    "New ride request",
                    f"Ride {ride.id} is available. Please accept or decline."))

                # Wait for driver response with polling
                start_time = time.time()
                while (time.time() - start_time) < DRIVER_RESPONSE_TIMEOUT_SEC:
                    current_ride = self._ride_repository.find_by_id(ride.id)
                    if not current_ride:
                        break

                    if (current_ride.status == RideStatus.ACCEPTED and
                            current_ride.driver_id == latest_driver.id):
                        return latest_driver

                    if current_ride.status == RideStatus.CANCELLED:
                        return None

                    if (current_ride.driver_id and
                            current_ride.driver_id != latest_driver.id):
                        break  # Another driver was assigned

                    time.sleep(0.5)  # Poll every 500ms

                # Final check after timeout
                final_ride = self._ride_repository.find_by_id(ride.id)
                if final_ride:
                    if (final_ride.status == RideStatus.ACCEPTED and
                            final_ride.driver_id == latest_driver.id):
                        return latest_driver
                    if final_ride.status == RideStatus.CANCELLED:
                        return None

            finally:
                self._lock_service.release(lock_key)

        return None
    
    def release_driver(self, driver_id: Optional[str]) -> None:
        if not driver_id:
            return
        driver = self._driver_repository.find_by_id(driver_id)
        if driver:
            driver.status = DriverStatus.ONLINE
            self._driver_repository.save(driver)