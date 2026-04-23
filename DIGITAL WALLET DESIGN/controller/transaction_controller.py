

from typing import Dict

from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from service.transaction_service import TransactionService


class TransactionController:
    def __init__(self, transaction_service: TransactionService):
        self._transaction_service = transaction_service


    def transfer(self, from_account_number: str, to_account_number: str,amount_minor: int, description: str) -> Transaction:
        return self._transaction_service.transfer(
            from_account_number, to_account_number, amount_minor, description)

    def initiate_deposit(self, account_number: str, amount_minor: int,
                         payment_method: str, payment_gateway: str,
                         payment_details: Dict[str, str]) -> Transaction:
        return self._transaction_service.initiate_deposit(
            account_number, amount_minor, payment_method, payment_gateway, payment_details)
    
    def handle_payment_callback(self, provider_ref: str, status: TransactionStatus):
        self._transaction_service.handle_deposit_callback(provider_ref, status)

    def withdraw(self, account_number: str, amount_minor: int,
                 description: str) -> Transaction:
        return self._transaction_service.withdraw(account_number, amount_minor, description)

