from typing import List, Optional, TYPE_CHECKING
from domain.recovery_status import RecoveryStatus
from service.recovery_service import RecoveryService

if TYPE_CHECKING:
    from domain.state.vending_machine_state import VendingMachineState

class RecoveryController:
    def __init__(self, service: RecoveryService):
        self.recovery_service = service
        print("RecoveryController initialized")

    def check_and_recover_machine(self, machine_id: int):
        self.recovery_service.perform_recovery(machine_id)

    def get_recovery_status(self, machine_id: int) -> RecoveryStatus:
        return self.recovery_service.get_recovery_status(machine_id)

    def create_recovery_entry(self, machine_id: int, transaction_id: int, state_name: str):
        self.recovery_service.create_recovery_entry(machine_id, transaction_id, state_name)

    def check_and_recover_all(self):
        self.recovery_service.check_and_recover()
