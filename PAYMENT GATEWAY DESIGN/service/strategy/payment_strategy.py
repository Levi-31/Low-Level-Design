from abc import ABC, abstractmethod

from domain.payment_request import PaymentRequest
from domain.payment_response import PaymentResponse
from domain.transaction import Transaction
from service.template.payment_gateway import PaymentGateway



class PaymentStrategy(ABC):
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    @abstractmethod
    def process_payment(self, payment_request:PaymentRequest, transaction:Transaction) -> PaymentResponse:
        pass
