from abc import ABC, abstractmethod
from typing import Dict


class PaymentGatewayProvider(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def initiate_payment(self, account_number: str, amount_minor: int,
                         payment_method: str, payment_details: Dict[str, str]) -> str:
        pass

    @abstractmethod
    def verify_callback(self, provider_ref: str, status: str) -> bool:
        pass