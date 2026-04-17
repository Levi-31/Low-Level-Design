from domain.recovery_status import RecoveryStatus

class Recovery:
    def __init__(self, id: int, vending_machine_id: int, last_transaction_id: int, last_state: str):
        self.id = id
        self.vending_machine_id = vending_machine_id
        self.last_transaction_id = last_transaction_id
        self.last_state = last_state
        self.status = RecoveryStatus.PENDING

    def __str__(self):
        return f"Recovery {self.id} for Machine {self.vending_machine_id} - Last State: {self.last_state}"