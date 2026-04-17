from typing import List, Dict, Any, Optional
from repository.vending_machine_repository import VendingMachineRepository
from repository.product_repository import ProductRepository
from domain.product import Product

class VendingMachineService:
    def __init__(self, vm_repo: VendingMachineRepository, p_repo: ProductRepository):
        self.vending_machine_repository = vm_repo
        self.product_repository = p_repo
        print("VendingMachineService initialized")

    def get_available_products(self, machine_id: int) -> List[Product]:
        print(f"VendingMachineService: Getting available products for machine {machine_id}")
        machine = self.vending_machine_repository.find_by_id(machine_id)
        if machine:
            return [p for p, q in machine.inventory.values() if q > 0]
        return []

    def get_product_details(self, machine_id: int, product_id: int) -> Optional[Product]:
        return self.product_repository.find_by_id(product_id)

    def update_inventory(self, machine_id: int, product_id: int, quantity: int):
        machine = self.vending_machine_repository.find_by_id(machine_id)
        product = self.product_repository.find_by_id(product_id)
        if machine and product:
            machine.add_product(product, quantity)

    def is_product_available(self, machine_id: int, product_id: int) -> bool:
        machine = self.vending_machine_repository.find_by_id(machine_id)
        return machine.has_product(product_id) if machine else False
