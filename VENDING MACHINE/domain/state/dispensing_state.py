from domain.state.vending_machine_state import VendingMachineState

class DispensingState(VendingMachineState):
    def process_payment(self, machine, request):
        return None

    def cancel_payment(self, machine, transaction_id: int):
        pass

    @property
    def state_name(self) -> str:
        return "DISPENSING"