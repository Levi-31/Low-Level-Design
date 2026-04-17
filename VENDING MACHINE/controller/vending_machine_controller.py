from typing import List, Optional
from service.vending_machine_service import VendingMachineService
from domain.product import Product

class VendingMachineController:
    def __init__(self, service: VendingMachineService):
        self.vending_machine_service = service
        print("VendingMachineController initialized")

    def get_available_products(self, machine_id: int) -> List[Product]:
        return self.vending_machine_service.get_available_products(machine_id)

    def get_product_details(self, machine_id: int, product_id: int) -> Optional[Product]:
        return self.vending_machine_service.get_product_details(machine_id, product_id)
