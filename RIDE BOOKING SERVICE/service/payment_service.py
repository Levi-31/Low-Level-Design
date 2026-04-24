


from domain.notification_message import NotificationMessage
from domain.payment_status import PaymentStatus
from domain.payment_type import PaymentType
from domain.ride import Ride
from repository.ride_repository import RideRepository
from service.notification.notification_service import NotificationService


class PaymentService:
    def __init__(self, ride_repository: RideRepository,
                 notification_service: NotificationService):
        self._ride_repository = ride_repository
        self._notification_service = notification_service
        self._ride_to_payment_id: dict = {}  # ride_id -> transaction_id
        self._counter = 1000

    def _generate_id(self) -> str:
        self._counter += 1
        return f"txn-{self._counter}"
    
    def _find_ride_id(self, transaction_id: str) -> str:
        for ride_id, pay_id in self._ride_to_payment_id.items():
            if pay_id == transaction_id:
                return ride_id
        raise ValueError(f"Unknown transaction id: {transaction_id}")
    
    def initiate_payment(self, ride: Ride) -> str:
        if ride.payment_type != PaymentType.PRE_PAYMENT:
            raise Exception("Only PRE_PAYMENT rides can initiate payment")
        transaction_id = self._generate_id()
        ride.payment_status = PaymentStatus.PENDING
        ride.payment_id = transaction_id
        self._ride_repository.save(ride)
        self._ride_to_payment_id[ride.id] = transaction_id
        # TODO: Integrate with external gateway.
        print(f"[Payment] Initiated payment for ride {ride.id} transaction={transaction_id}")
        return transaction_id
    
    def handle_payment_callback(self, transaction_id: str, status: PaymentStatus) -> Ride:
        ride_id = self._find_ride_id(transaction_id)
        del self._ride_to_payment_id[ride_id]
        ride = self._ride_repository.find_by_id(ride_id)
        if not ride:
            raise ValueError(f"Ride not found for transaction: {transaction_id}")
        ride.payment_status = status
        self._ride_repository.save(ride)
        status_str = status.name
        self._notification_service.send(NotificationMessage(
            ride.rider_id,
            f"Payment {status_str}",
            f"Payment status for ride {ride.id} is {status_str}"))
        return ride