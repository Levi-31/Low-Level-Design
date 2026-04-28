from domain.payment_request import PaymentRequest
from domain.payment_response import PaymentResponse
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from repository.payment_repository import PaymentRepository
from repository.user_repository import UserRepository
from service.factory.payment_factory import PaymentFactory
from service.locking_service import LockService
from service.strategy.payment_strategy import PaymentStrategy


class PaymentService:
    def __init__(self,payment_repository:PaymentRepository,user_repository : UserRepository,locking_service:LockService):
        self.payment_repository = payment_repository
        self.user_repository = user_repository
        self.locking_service = locking_service
    

    def get_payment_strategy(self,payment_request:PaymentRequest) -> PaymentStrategy:
        gateway = payment_request.gateway
        method = payment_request.payment_method

        gateway_instance = PaymentFactory.get_gateway(gateway)

        if not gateway_instance.supports(method):
            raise ValueError(f"{gateway} does not support {method}")

        strategy = PaymentFactory.get_payment_strategy(
            method,
            gateway_instance
        )

        return strategy
    

    def process_payment(self, payment_request: PaymentRequest) -> PaymentResponse:

        user = self.user_repository.find_by_id(payment_request.user_id)
        if not user:
            raise ValueError(f"User with ID {payment_request.user_id} not found.")

        lock_key = f"req:{payment_request.request_id}"

        if not self.locking_service.acquire(lock_key, timeout_ms=200):
            raise Exception("Duplicate request in progress")

        try:
            strategy = self.get_payment_strategy(payment_request)

            transaction = Transaction(
                id="txn_" + payment_request.request_id,
                payment_id="pay_" + payment_request.request_id,
                gateway=payment_request.gateway,
                payment_method=payment_request.payment_method,
                status=TransactionStatus.INITIATED,
                user_id=payment_request.user_id,
                request_id=payment_request.request_id
            )
            self.payment_repository.save(transaction)

            try:
                response = strategy.process_payment(payment_request,transaction)
            finally:
                self.payment_repository.save(transaction)

            return response

        finally:
            self.locking_service.release(lock_key)
    

    def handle_call_back(self, gateway_transaction_id: str, status: TransactionStatus):

        lock_key = f"cb:{gateway_transaction_id}"

        if not self.locking_service.acquire(lock_key, timeout_ms=200):
            raise Exception("Callback already being processed")

        try:
            tx = self.payment_repository.find_by_gateway_transaction_id(gateway_transaction_id)

            if tx is None:
                raise ValueError(
                    f"Transaction not found for providerRef: {gateway_transaction_id}"
                )

            if tx.status in (TransactionStatus.SUCCESS, TransactionStatus.FAILED):
                return

            if status == TransactionStatus.SUCCESS:
                tx.status = (TransactionStatus.SUCCESS)

            elif status == TransactionStatus.FAILED:
                tx.status = (TransactionStatus.FAILED)

            self.payment_repository.save(tx)

        finally:
            self.locking_service.release(lock_key)
