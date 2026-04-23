




from contextlib import contextmanager
import time

from domain.driver_status import DriverStatus
from domain.fare_estimate_response import FareEstimateResponse
from domain.location import Location
from domain.notification_message import NotificationMessage
from domain.payment_status import PaymentStatus
from domain.payment_type import PaymentType
from domain.ride import Ride
from domain.ride_request import RideRequest
from domain.ride_status import RideStatus
from domain.ride_status_response import RideStatusResponse
from domain.state.ride_state_machine import RideStateMachine
from repository.driver_repository import DriverRepository
from repository.ride_repository import RideRepository
from repository.rider_repository import RiderRepository
from service.location_service import LocationService
from service.lock_service import LockService
from service.matching_service import MatchingService
from service.notification.notification_service import NotificationService
from service.payment_service import PaymentService
from service.pricing_service import PricingService

def _now_ms() -> int:
    return int(time.time() * 1000)


_ride_counter = [0]


def _generate_ride_id() -> str:
    _ride_counter[0] += 1
    return f"ride-{_ride_counter[0]}"

class RideService:
    def __init__(self, ride_repository: RideRepository,
                 rider_repository: RiderRepository,
                 driver_repository: DriverRepository,
                 matching_service: MatchingService,
                 pricing_service: PricingService,
                 payment_service: PaymentService,
                 notification_service: NotificationService,
                 location_service: LocationService,
                 lock_service: LockService):
        
        self._ride_repository = ride_repository
        self._rider_repository = rider_repository
        self._driver_repository = driver_repository
        self._matching_service = matching_service
        self._pricing_service = pricing_service
        self._payment_service = payment_service
        self._notification_service = notification_service
        self._location_service = location_service
        self._lock_service = lock_service
        self._ride_state_machine = RideStateMachine()


    @contextmanager
    def _ride_lock(self, ride_id: str):
        lock_key = f"ride_lock_{ride_id}"
        acquired = self._lock_service.acquire(lock_key, 500)
        if not acquired:
            raise RuntimeError(f"Could not acquire lock for ride: {ride_id}")
        try:
            yield
        finally:
            self._lock_service.release(lock_key)

    def _validate_request(self, request: RideRequest) -> None:
        rider = self._rider_repository.find_by_id(request.rider_id)
        if not rider:
            raise ValueError(f"Rider not found: {request.rider_id}")
        pickup = request.pickup_location
        drop = request.dropoff_location
        if (abs(pickup.latitude - drop.latitude) < 0.0001 and
                abs(pickup.longitude - drop.longitude) < 0.0001):
            raise ValueError("Pickup and dropoff cannot be the same")
        
    def _start_matching(self, ride: Ride) -> None:
        matched = self._matching_service.match_driver(ride)
        if not matched:
            print(f"[Matching] No drivers available for ride {ride.id}")


    def request_ride(self, request: RideRequest) -> Ride:
        self._validate_request(request)
        distance_km = max(0.5, self._location_service.calculate_distance_km(
            request.pickup_location, request.dropoff_location))
        duration_sec = max(300, self._location_service.estimate_duration_sec(distance_km))
        estimated_fare = self._pricing_service.estimate_fare(
            request.pickup_location, request.dropoff_location,
            distance_km, duration_sec).estimated_fare

        ride = Ride(_generate_ride_id(), request.rider_id,
                    request.pickup_location, request.dropoff_location,
                    request.payment_type, _now_ms())
        ride.estimated_distance_km = distance_km
        ride.estimated_duration_sec = duration_sec
        ride.estimated_fare = estimated_fare
        ride.payment_status = (PaymentStatus.PENDING if request.payment_type == PaymentType.PRE_PAYMENT else PaymentStatus.NONE)
        self._ride_repository.save(ride)

        if request.payment_type == PaymentType.PRE_PAYMENT:
            self._payment_service.initiate_payment(ride)
        else:
            self._start_matching(ride)

        return ride

    def estimate_fare(self, pickup: Location, dropoff: Location) -> FareEstimateResponse:
        distance_km = max(0.5, self._location_service.calculate_distance_km(pickup, dropoff))
        duration_sec = max(300, self._location_service.estimate_duration_sec(distance_km))
        return self._pricing_service.estimate_fare(pickup, dropoff, distance_km, duration_sec)

    def handle_payment_callback(self, transaction_id: str, status: PaymentStatus) -> Ride:
        ride = self._payment_service.handle_payment_callback(transaction_id, status)
        if status == PaymentStatus.COMPLETED:
            self._start_matching(ride)
        elif status == PaymentStatus.FAILED:
            self._ride_state_machine.transition(ride, RideStatus.CANCELLED)
            ride.cancelled_at = _now_ms()
            self._ride_repository.save(ride)
        return ride


    def get_ride_status(self, ride_id: str) -> RideStatusResponse:
        ride = self._ride_repository.find_by_id(ride_id)
        if not ride:
            raise ValueError(f"Ride not found: {ride_id}")
        driver = None
        if ride.driver_id:
            driver = self._driver_repository.find_by_id(ride.driver_id)
        return RideStatusResponse(
            ride.id, ride.status,
            driver.id if driver else None,
            driver.name if driver else None,
            driver.current_location if driver else None,
            ride.estimated_fare, _now_ms())

    def driver_accept(self, ride_id: str, driver_id: str) -> None:
        with self._ride_lock(ride_id):
            ride = self._ride_repository.find_by_id(ride_id)
            if not ride:
                raise ValueError(f"Ride not found: {ride_id}")

            if ride.status == RideStatus.REQUESTED:
                ride.driver_id = driver_id
                ride.assigned_at = _now_ms()
                self._ride_state_machine.transition(ride, RideStatus.ASSIGNED)

            if ride.driver_id != driver_id:
                raise RuntimeError("Driver not assigned to ride")

            driver = self._driver_repository.find_by_id(driver_id)
            if driver:
                driver.status = DriverStatus.ON_RIDE
                self._driver_repository.save(driver)

            self._ride_state_machine.transition(ride, RideStatus.ACCEPTED)
            ride.accepted_at = _now_ms()
            self._ride_repository.save(ride)


            self._notification_service.send(NotificationMessage(
                ride.rider_id, "Driver accepted",
                f"Driver {driver_id} accepted ride {ride_id}"))


    def driver_decline(self, ride_id: str, driver_id: str) -> None:
        with self._ride_lock(ride_id):
            ride = self._ride_repository.find_by_id(ride_id)
            if not ride:
                raise ValueError(f"Ride not found: {ride_id}")
            if ride.status == RideStatus.REQUESTED:
                return  # Matching continues

    def start_ride(self, ride_id: str, driver_id: str) -> None:
        with self._ride_lock(ride_id):
            ride = self._ride_repository.find_by_id(ride_id)
            if not ride:
                raise ValueError(f"Ride not found: {ride_id}")
            if ride.driver_id != driver_id:
                raise RuntimeError("Driver mismatch")
            self._ride_state_machine.transition(ride, RideStatus.IN_PROGRESS)
            ride.started_at = _now_ms()
            self._ride_repository.save(ride)


    def complete_ride(self, ride_id: str, driver_id: str) -> None:
        with self._ride_lock(ride_id):
            ride = self._ride_repository.find_by_id(ride_id)
            if not ride:
                raise ValueError(f"Ride not found: {ride_id}")
            if ride.driver_id != driver_id:
                raise RuntimeError("Driver mismatch")
            self._ride_state_machine.transition(ride, RideStatus.COMPLETED)
            ride.completed_at = _now_ms()
            dist_km = max(0.5, self._location_service.calculate_distance_km(
                ride.pickup_location, ride.dropoff_location))
            ride.actual_distance_km = dist_km
            dur_sec = max(ride.estimated_duration_sec,
                          self._location_service.estimate_duration_sec(dist_km))
            ride.actual_duration_sec = dur_sec
            if ride.payment_type == PaymentType.POST_PAYMENT:
                ride.payment_status = PaymentStatus.COMPLETED
            elif ride.payment_status != PaymentStatus.COMPLETED:
                ride.payment_status = PaymentStatus.COMPLETED

                
            self._ride_repository.save(ride)
            self._matching_service.release_driver(driver_id)
            self._notification_service.send(NotificationMessage(
                ride.rider_id, "Trip completed",
                f"Fare charged: {ride.estimated_fare}"))


    def cancel_ride(self, ride_id: str, reason: str) -> None:
        with self._ride_lock(ride_id):
            ride = self._ride_repository.find_by_id(ride_id)
            if not ride:
                raise ValueError(f"Ride not found: {ride_id}")
            if ride.status in (RideStatus.COMPLETED, RideStatus.CANCELLED):
                return
            if ride.driver_id:
                self._matching_service.release_driver(ride.driver_id)
            self._ride_state_machine.transition(ride, RideStatus.CANCELLED)
            ride.cancelled_at = _now_ms()
            ride.cancellation_reason = reason
            self._ride_repository.save(ride)
