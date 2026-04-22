




import time
import uuid

from domain.booking import Booking
from domain.booking_status import BookingStatus
from domain.date_range import DateRange
from domain.transaction_status import TransactionStatus
from repository.booking_repository import BookingRepository
from repository.cancellation_policy_repository import CancellationPolicyRepository
from repository.hotel_repository import HotelRepository
from repository.room_type_repository import RoomTypeRepository
from repository.user_repository import UserRepository
from service.booking_state_handler import BookingStateHandler
from service.inventory_service import InventoryService
from service.policy_service import PolicyService
from service.pricing_service import PricingService
from service.transaction_service import TransactionService


class BookingService:
    def __init__(self, booking_repo: BookingRepository, hotel_repo: HotelRepository,
                 room_type_repo: RoomTypeRepository, user_repo: UserRepository,
                 inventory_ser: InventoryService, pricing_ser: PricingService,
                 policy_ser: PolicyService, cancellation_policy_repo: CancellationPolicyRepository,
                 transaction_ser:TransactionService): # TransactionService passed as object to avoid circular import if any
        self.booking_repo = booking_repo
        self.hotel_repo = hotel_repo
        self.room_type_repo = room_type_repo
        self.user_repo = user_repo
        self.inventory_ser = inventory_ser
        self.pricing_ser = pricing_ser
        self.policy_ser = policy_ser
        self.cancellation_policy_repo = cancellation_policy_repo
        self.transaction_ser = transaction_ser



    def create_booking(self, user_id: str, hotel_id: str, room_type_id: str, 
                       date_range: DateRange, expected_total_price: int) -> Booking:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f"User not found: {user_id}")

        room_type = self.room_type_repo.find_by_id(room_type_id)
        if not room_type:
            raise ValueError(f"RoomType not found: {room_type_id}")

        if date_range.check_in_date_utc >= date_range.check_out_date_utc:
            raise ValueError("Invalid date range")

        if not self.inventory_ser.check_availability(hotel_id, room_type_id, date_range, 1):
            raise ValueError("No availability")

        nightly_prices = self.pricing_ser.rate_stay(hotel_id, room_type_id, date_range)
        if not nightly_prices:
            raise ValueError("Could not fetch prices")
        
        calculated_total = self.pricing_ser.compute_total(nightly_prices)
        if expected_total_price > 0 and abs(calculated_total - expected_total_price) > 100:
            raise ValueError(f"Price mismatch: expected {expected_total_price}, got {calculated_total}")
        
        now = int(time.time() * 1000)
        booking_id = str(uuid.uuid4())
        booking = Booking(
            id=booking_id,
            user_id=user_id,
            hotel_id=hotel_id,
            room_type_id=room_type_id,
            check_in_date_utc=date_range.check_in_date_utc,
            check_out_date_utc=date_range.check_out_date_utc,
            nightly_prices=nightly_prices,
            total_amount_minor=calculated_total,
            booking_status=BookingStatus.CREATED,
            payment_status=TransactionStatus.PENDING,
            created_at=now
        )

        return self.booking_repo.save(booking)


    def cancel_booking(self, booking_id: str, user_id: str):
        booking = self.booking_repo.find_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking not found: {booking_id}")

        if booking.user_id != user_id:
            raise ValueError("User does not own this booking")

        if not BookingStateHandler.can_cancel(booking):
            raise ValueError(f"Cannot cancel booking in state: {booking.booking_status}")

        hotel = self.hotel_repo.find_by_id(booking.hotel_id)
        if not hotel:
            raise ValueError("Hotel not found")

        policy = self.cancellation_policy_repo.find_by_id(hotel.cancellation_policy_id)
        if not policy:
            raise ValueError("Cancellation policy not found")
        
        now = int(time.time() * 1000)
        refund_decision = self.policy_ser.evaluate_cancellation(booking, policy, now)

        BookingStateHandler.transition(booking, BookingStatus.CANCELLED)
        if refund_decision.refund_amount_minor > 0:
            booking.payment_status = TransactionStatus.REFUNDED
            self.transaction_ser.issue_refund(booking_id, refund_decision.refund_amount_minor)

        self.booking_repo.save(booking)


    def check_in(self, booking_id: str, room_id: str, check_in_time_utc: int) -> Booking:
        booking = self.booking_repo.find_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")

        BookingStateHandler.require_status(booking, BookingStatus.CONFIRMED)

        booking.allocated_room_id = room_id
        booking.check_in_time_utc = check_in_time_utc
        BookingStateHandler.transition(booking, BookingStatus.CHECKED_IN)

        return self.booking_repo.save(booking)

    def check_out(self, booking_id: str, check_out_time_utc: int) -> Booking:
        booking = self.booking_repo.find_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")

        BookingStateHandler.require_status(booking, BookingStatus.CHECKED_IN)

        booking.check_out_time_utc = check_out_time_utc
        BookingStateHandler.transition(booking, BookingStatus.CHECKED_OUT)

        return self.booking_repo.save(booking)
    