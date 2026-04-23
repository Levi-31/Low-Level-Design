





import time

from controller.driver_controller import DriverController
from controller.payment_controller import PaymentController
from controller.ride_controller import RideController
from domain.driver import Driver
from domain.driver_status import DriverStatus
from domain.location import Location
from domain.payment_status import PaymentStatus
from domain.payment_type import PaymentType
from domain.ride_request import RideRequest
from domain.rider import Rider
from domain.strategy.base_pricing_strategy import BasePricingStrategy
from domain.strategy.nerarest_driver_strategy import NearestDriverStrategy
from repository.implementation.driver_repository_implementation import InMemoryDriverRepository
from repository.implementation.location_repository_implementation import InMemoryLocationRepository
from repository.implementation.ride_repository_implementation import InMemoryRideRepository
from repository.implementation.rider_repository_implementation import InMemoryRiderRepository
from service.driver_service import DriverService
from service.location_service import LocationService
from service.lock_service import LockService
from service.matching_service import MatchingService
from service.notification.notification_service import NotificationService
from service.payment_service import PaymentService
from service.pricing_service import PricingService
from service.ride_service import RideService


def current_time_ms() -> int:
    return int(time.time() * 1000)


def main():
    # ---- Repositories ----
    ride_repository = InMemoryRideRepository()
    rider_repository = InMemoryRiderRepository()
    driver_repository = InMemoryDriverRepository()
    location_repository = InMemoryLocationRepository()

    # ---- Seed Data ----
    rider = Rider("rider-1", "Alice Rider", "alice@example.com", "111-222-3333", current_time_ms())
    rider_repository.save(rider)

    driver = Driver("driver-1", "Bob Driver", "bob@example.com", "444-555-6666",
                    "KA01AB1234", "Sedan", DriverStatus.ONLINE)
    driver.current_location = Location(37.7749, -122.4194, "Market St", current_time_ms())
    driver_repository.save(driver)

    # ---- Services ----
    notification_service = NotificationService()
    pricing_service = PricingService(BasePricingStrategy())
    location_service = LocationService(location_repository)
    lock_service = LockService()
    matching_service = MatchingService(
        driver_repository, ride_repository,
        NearestDriverStrategy(), lock_service, notification_service)
    payment_service = PaymentService(ride_repository, notification_service)
    ride_service = RideService(
        ride_repository, rider_repository, driver_repository,
        matching_service, pricing_service, payment_service,
        notification_service, location_service, lock_service)
    driver_service = DriverService(driver_repository)

    import pdb;pdb.set_trace()
    # ---- Controllers ----
    ride_controller = RideController(ride_service)
    driver_controller = DriverController(driver_service, ride_service)
    payment_controller = PaymentController(ride_service)

    # ---- Scenario 1: PRE_PAYMENT ride ----
    pickup = Location(37.7749, -122.4194, "Market St", current_time_ms())
    drop = Location(37.7840, -122.4090, "Mission St", current_time_ms())

    print("--- Requesting ride with PRE_PAYMENT ---")
    pre_pay_req = RideRequest(rider.id, pickup, drop, PaymentType.PRE_PAYMENT)
    ride = ride_controller.request_ride(pre_pay_req)
    print(f"Ride created with id {ride.id} paymentId={ride.payment_id}")

    payment_controller.handle_callback(ride.payment_id, PaymentStatus.COMPLETED)
    driver_controller.accept_ride(ride.id, driver.id)
    driver_controller.start_ride(ride.id, driver.id)
    driver_controller.complete_ride(ride.id, driver.id)

    completed_status = ride_controller.get_ride_status(ride.id)
    print(f"Ride status: {completed_status.status.name} fare={completed_status.estimated_fare}")

    # ---- Scenario 2: POST_PAYMENT (cash) ride ----
    print("--- Requesting ride with POST_PAYMENT (cash) ---")
    post_pay_req = RideRequest(rider.id, pickup, drop, PaymentType.POST_PAYMENT)
    cash_ride = ride_controller.request_ride(post_pay_req)
    driver_controller.accept_ride(cash_ride.id, driver.id)
    driver_controller.start_ride(cash_ride.id, driver.id)
    driver_controller.complete_ride(cash_ride.id, driver.id)

    cash_status = ride_controller.get_ride_status(cash_ride.id)
    print(f"Cash ride status: {cash_status.status.name} fare={cash_status.estimated_fare}")


if __name__ == "__main__":
    main()
