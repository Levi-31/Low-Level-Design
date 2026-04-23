

from domain.payment_status import PaymentStatus
from service.ride_service import RideService


class PaymentController:
    def __init__(self, ride_service: RideService):
        self._ride_service = ride_service

    def handle_callback(self, transaction_id: str, status: PaymentStatus) -> None:
        self._ride_service.handle_payment_callback(transaction_id, status)