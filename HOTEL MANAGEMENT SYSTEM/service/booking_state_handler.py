




from typing import List, Set, Tuple

from domain.booking import Booking
from domain.booking_status import BookingStatus


class BookingStateHandler:
    # Define valid state transitions as a set of (from, to) tuples
    VALID_TRANSITIONS: Set[Tuple[BookingStatus, BookingStatus]] = {
        (BookingStatus.CREATED, BookingStatus.HELD),
        (BookingStatus.HELD, BookingStatus.CONFIRMED),
        (BookingStatus.HELD, BookingStatus.CANCELLED),
        (BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN),
        (BookingStatus.CHECKED_IN, BookingStatus.CHECKED_OUT),
        (BookingStatus.CREATED, BookingStatus.CANCELLED),
        (BookingStatus.CONFIRMED, BookingStatus.CANCELLED),
    }

    @staticmethod
    def can_transition(current_status: BookingStatus, new_status: BookingStatus) -> bool:
        if current_status == new_status:
            return True
        return (current_status, new_status) in BookingStateHandler.VALID_TRANSITIONS

    @staticmethod
    def transition(booking: Booking, new_status: BookingStatus):
        current_status = booking.booking_status
        if not BookingStateHandler.can_transition(current_status, new_status):
            raise ValueError(f"Invalid state transition: Cannot transition from {current_status} to {new_status}")
        booking.booking_status = new_status

    @staticmethod
    def require_status(booking: Booking, expected_status: BookingStatus):
        if booking.booking_status != expected_status:
            raise ValueError(f"Booking must be in {expected_status} status. Current status: {booking.booking_status}")

    @staticmethod
    def require_any_status(booking: Booking, allowed_statuses: List[BookingStatus]):
        if booking.booking_status not in allowed_statuses:
            raise ValueError(f"Booking must be in one of {allowed_statuses}. Current status: {booking.booking_status}")

    @staticmethod
    def can_cancel(booking: Booking) -> bool:
        status = booking.booking_status
        return status in [BookingStatus.CREATED, BookingStatus.HELD, BookingStatus.CONFIRMED]

    @staticmethod
    def can_check_in(booking: Booking) -> bool:
        return booking.booking_status == BookingStatus.CONFIRMED

    @staticmethod
    def can_check_out(booking: Booking) -> bool:
        return booking.booking_status == BookingStatus.CHECKED_IN

    @staticmethod
    def can_initiate_transaction(booking: Booking) -> bool:
        return booking.booking_status == BookingStatus.CREATED

    @staticmethod
    def counts_in_inventory(booking: Booking) -> bool:
        status = booking.booking_status
        return status in [BookingStatus.HELD, BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN]
