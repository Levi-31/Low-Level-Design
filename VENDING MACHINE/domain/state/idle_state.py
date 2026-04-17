import time
from domain.state.dispensing_state import DispensingState
from domain.state.payment_processing_state import ProcessingPaymentState
from domain.state.vending_machine_state import VendingMachineState
from domain.transaction import Transaction



class IdleState(VendingMachineState):
    def process_payment(self, machine, request) -> Transaction:
        print(f"IdleState: Processing payment request for product {request.product_id}")
        
        transaction = Transaction(1, machine.id, request.product_id, request.total_amount)
        machine.current_transaction = transaction
        
        # Simulating payment processing
        transaction.add_payment(request.total_amount)
        for denom, count in request.denominations.items():
            machine.add_cash(denom, count)
            
        machine.set_state(ProcessingPaymentState())
        time.sleep(1)
        
        machine.set_state(DispensingState())
        if machine.has_product(request.product_id):
            machine.dispense_product(request.product_id)
            machine.set_state(IdleState())
            
        print(f"IdleState: Payment processed, transaction created: {transaction.id}")
        return transaction

    def cancel_payment(self, machine, transaction_id: int):
        print("IdleState: No active transaction to cancel")

    @property
    def state_name(self) -> str:
        return "IDLE"
