


from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from service.transaction_service import TransactionService


class TransactionController:
    def __init__(self, transaction_ser: TransactionService):
        self.transaction_ser = transaction_ser

    def initiate_transaction(self, booking_id: str) -> Transaction:
        return self.transaction_ser.initiate_transaction(booking_id)

    def handle_transaction_callback(self, provider_ref: str, status: TransactionStatus):
        self.transaction_ser.handle_callback(provider_ref, status)