from typing import List, Optional, TYPE_CHECKING
from repository.vending_machine_repository import VendingMachineRepository
from repository.recovery_repository import RecoveryRepository
from repository.payment_repository import PaymentRepository
from domain.recovery import Recovery
from domain.recovery_status import RecoveryStatus

if TYPE_CHECKING:
    from domain.state.vending_machine_state import VendingMachineState

class RecoveryService:
    def __init__(self, vm_repo: VendingMachineRepository, r_repo: RecoveryRepository, p_repo: PaymentRepository):
        self.vending_machine_repository = vm_repo
        self.recovery_repository = r_repo
        self.payment_repository = p_repo
        print("RecoveryService initialized")

    def perform_recovery(self, machine_id: int):
        print(f"RecoveryService: Performing recovery for machine {machine_id}")

    def get_recovery_status(self, machine_id: int) -> RecoveryStatus:
        recovery = self.recovery_repository.find_by_machine_id(machine_id)
        return recovery.status if recovery else RecoveryStatus.COMPLETED

    def create_recovery_entry(self, machine_id: int, transaction_id: int, state_name: str):
        recovery = Recovery(1, machine_id, transaction_id, state_name)
        self.recovery_repository.save(recovery)

    def check_and_recover(self):
        print("RecoveryService: System-wide recovery check")
