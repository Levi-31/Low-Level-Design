from domain.payment_request import PaymentRequest
from domain.transaction_status import TransactionStatus
from service.payment_service import PaymentService


class PaymentController:
    def __init__(self,payment_service:PaymentService):
        self.payment_service = payment_service

    
    def process_payment(self,payment_request:PaymentRequest):
        return self.payment_service.process_payment(payment_request)
    
    def handle_payment_callback(self, provider_ref: str, status: TransactionStatus):
        self.payment_service.handle_call_back(provider_ref, status)


    