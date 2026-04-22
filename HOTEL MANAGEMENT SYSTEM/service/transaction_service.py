



import time
import uuid

from domain.booking_status import BookingStatus
from domain.date_range import DateRange
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from repository.booking_repository import BookingRepository
from repository.transaction_repository import TransactionRepository
from service.booking_state_handler import BookingStateHandler
from service.inventory_service import InventoryService


class TransactionService:
    def __init__(self, transaction_repo: TransactionRepository, booking_repo: BookingRepository,
                 inventory_ser: InventoryService):
        self.transaction_repo = transaction_repo
        self.booking_repo = booking_repo
        self.inventory_ser = inventory_ser
    

    def initiate_transaction(self, booking_id: str) -> Transaction:
        booking = self.booking_repo.find_by_id(booking_id)
        if not booking:
            raise ValueError(f"Booking not found: {booking_id}")

        BookingStateHandler.require_status(booking, BookingStatus.CREATED)

        date_range = DateRange(booking.check_in_date_utc, booking.check_out_date_utc)
        if not self.inventory_ser.check_availability(booking.hotel_id, booking.room_type_id, date_range, 1):
            raise ValueError("No availability")

        BookingStateHandler.transition(booking, BookingStatus.HELD)
        now = int(time.time() * 1000)
        booking.hold_expires_at = now + 15 * 60 * 1000 # 15 minutes TTL
        self.booking_repo.save(booking)

        transaction_id = str(uuid.uuid4())
        transaction = Transaction(
            id=transaction_id,
            booking_id=booking_id,
            amount_minor=booking.total_amount_minor,
            currency="USD",
            status=TransactionStatus.PENDING,
            provider_ref=f"PG_REF_{transaction_id}",
            initiated_at=now
        )

        return self.transaction_repo.save(transaction)
    


    def handle_callback(self, provider_ref: str, status: TransactionStatus):
        transaction = self.transaction_repo.find_by_provider_ref(provider_ref)
        if not transaction:
            raise ValueError(f"Transaction not found: {provider_ref}")

        if transaction.status in [TransactionStatus.COMPLETED, TransactionStatus.FAILED]:
            return

        booking = self.booking_repo.find_by_id(transaction.booking_id)
        if not booking:
            raise ValueError("Booking not found")

        if status == TransactionStatus.COMPLETED:
            transaction.status = TransactionStatus.COMPLETED
            transaction.completed_at = int(time.time() * 1000)
            BookingStateHandler.transition(booking, BookingStatus.CONFIRMED)
            booking.payment_status = TransactionStatus.COMPLETED
        else:
            transaction.status = TransactionStatus.FAILED
            BookingStateHandler.transition(booking, BookingStatus.CANCELLED)
            booking.payment_status = TransactionStatus.FAILED

        self.transaction_repo.save(transaction)
        self.booking_repo.save(booking)

    def issue_refund(self, booking_id: str, amount_minor: int):
        booking = self.booking_repo.find_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found")

        refund_transaction_id = str(uuid.uuid4())
        refund_transaction = Transaction(
            id=refund_transaction_id,
            booking_id=booking_id,
            amount_minor=amount_minor,
            currency="USD",
            status=TransactionStatus.REFUNDED,
            provider_ref=f"REFUND_{refund_transaction_id}",
            initiated_at=int(time.time() * 1000),
            refunded_at=int(time.time() * 1000)
        )

        self.transaction_repo.save(refund_transaction)