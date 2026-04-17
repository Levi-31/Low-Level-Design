from typing import Dict, Optional
from domain.vending_machine import VendingMachine

class VendingMachineRepository:
    def __init__(self):
        self._machines: Dict[int, VendingMachine] = {}

    def save(self, machine: VendingMachine):
        self._machines[machine.id] = machine

    def find_by_id(self, machine_id: int) -> Optional[VendingMachine]:
        return self._machines.get(machine_id)

    def update_inventory(self, machine_id: int, product_id: int, quantity: int):
        machine = self.find_by_id(machine_id)
        if machine:
            pass # Implement logic if needed
