

from domain.ride import Ride
from domain.ride_status import RideStatus


class RideStateMachine:
    """State machine for ride lifecycle transitions."""

    ALLOWED_TRANSITIONS = {
        RideStatus.REQUESTED:   {RideStatus.ASSIGNED, RideStatus.CANCELLED},
        RideStatus.ASSIGNED:    {RideStatus.ACCEPTED, RideStatus.CANCELLED, RideStatus.REQUESTED},
        RideStatus.ACCEPTED:    {RideStatus.IN_PROGRESS, RideStatus.CANCELLED},
        RideStatus.IN_PROGRESS: {RideStatus.COMPLETED, RideStatus.CANCELLED},
        RideStatus.COMPLETED:   set(),
        RideStatus.CANCELLED:   set(),
    }

    def transition(self, ride: Ride, next_status: RideStatus) -> None:
        current = ride.status
        allowed = self.ALLOWED_TRANSITIONS.get(current, set())
        if next_status not in allowed:
            raise ValueError(
                f"Invalid ride state transition from {current} to {next_status}"
            )
        ride.status = next_status