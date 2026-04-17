from typing import Dict, Optional
from repository.vending_machine_repository import VendingMachineRepository
from repository.payment_repository import PaymentRepository
from domain.payment_request import PaymentRequest
from domain.transaction import Transaction

class PaymentService:
    def __init__(self, vm_repo: VendingMachineRepository, p_repo: PaymentRepository):
        self.vending_machine_repository = vm_repo
        self.payment_repository = p_repo
        print("PaymentService initialized")

    def process_payment(self, machine_id: int, request: PaymentRequest) -> Optional[Transaction]:
        machine = self.vending_machine_repository.find_by_id(machine_id)
        if machine:
            transaction = machine.process_payment(request)
            if transaction:
                self.payment_repository.save(transaction)
            return transaction
        return None

    def cancel_payment(self, machine_id: int, transaction_id: int):
        machine = self.vending_machine_repository.find_by_id(machine_id)
        if machine:
            machine.cancel_payment(transaction_id)

    def get_total_cash_in_machine(self, machine_id: int) -> float:
        machine = self.vending_machine_repository.find_by_id(machine_id)
        return machine.cash_box.total_amount if machine else 0.0

    def get_cash_box_status(self, machine_id: int) -> Dict:
        machine = self.vending_machine_repository.find_by_id(machine_id)
        return machine.cash_box.denominations if machine else {}
