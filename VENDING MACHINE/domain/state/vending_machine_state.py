from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.vending_machine import VendingMachine
    from domain.payment_request import PaymentRequest
    from domain.transaction import Transaction

class VendingMachineState(ABC):
    @abstractmethod
    def process_payment(self, machine: 'VendingMachine', request: 'PaymentRequest') -> 'Transaction':
        pass

    @abstractmethod
    def cancel_payment(self, machine: 'VendingMachine', transaction_id: int):
        pass

    @property
    @abstractmethod
    def state_name(self) -> str:
        pass