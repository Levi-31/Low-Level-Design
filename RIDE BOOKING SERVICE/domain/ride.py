




from typing import Optional

from domain.location import Location
from domain.payment_status import PaymentStatus
from domain.payment_type import PaymentType
from domain.ride_status import RideStatus


class Ride:
    def __init__(self, ride_id: str, rider_id: str, pickup_location: Location, dropoff_location: Location, payment_type: PaymentType, requested_at: int):
        self.id = ride_id
        self.rider_id = rider_id
        self.driver_id: Optional[str] = None
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        self.status: RideStatus = RideStatus.REQUESTED
        self.payment_type = payment_type
        self.payment_status: PaymentStatus = PaymentStatus.NONE
        self.payment_id: Optional[str] = None
        self.estimated_fare: int = 0
        self.estimated_distance_km: float = 0.0
        self.actual_distance_km: float = 0.0
        self.estimated_duration_sec: int = 0
        self.actual_duration_sec: int = 0
        self.requested_at: int = requested_at
        self.assigned_at: int = 0
        self.accepted_at: int = 0
        self.started_at: int = 0
        self.completed_at: int = 0
        self.cancelled_at: int = 0
        self.cancellation_reason: Optional[str] = None


    def __repr__(self):
        return f"Ride(id={self.id!r}, status={self.status})"