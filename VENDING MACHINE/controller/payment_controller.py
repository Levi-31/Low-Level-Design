from typing import List, Optional, Dict
from service.payment_service import PaymentService
from domain.payment_request import PaymentRequest
from domain.transaction import Transaction

class PaymentController:
    def __init__(self, service: PaymentService):
        self.payment_service = service
        print("PaymentController initialized")

    def process_payment(self, machine_id: int, request: PaymentRequest) -> Optional[Transaction]:
        return self.payment_service.process_payment(machine_id, request)

    def get_total_cash_in_machine(self, machine_id: int) -> float:
        return self.payment_service.get_total_cash_in_machine(machine_id)

    def get_cash_box_status(self, machine_id: int) -> Dict:
        return self.payment_service.get_cash_box_status(machine_id)
