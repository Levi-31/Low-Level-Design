from abc import ABC, abstractmethod

from domain.payment_methods import PaymentMethod


class PaymentGateway(ABC):

    @abstractmethod
    def create_order(self, payment):
        pass

    @abstractmethod
    def authorize(self, payment):
        pass

    @abstractmethod
    def capture(self, payment):
        pass

    @abstractmethod
    def verify_webhook(self, payload, signature) -> bool:
        pass

    @abstractmethod
    def supports(self, method:PaymentMethod):
        pass
    