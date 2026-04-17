from typing import Dict, Any, List
from service.admin_service import AdminService
from service.vending_machine_service import VendingMachineService

class AdminController:
    def __init__(self, admin_service: AdminService, vm_service: VendingMachineService):
        self.admin_service = admin_service
        self.vending_machine_service = vm_service
        print("AdminController initialized")

    def restock_product(self, machine_id: int, product_id: int, quantity: int):
        self.admin_service.restock_product(machine_id, product_id, quantity)
        print(f"Admin: Restocked product {product_id} with quantity {quantity}")

    def collect_cash(self, machine_id: int):
        result = self.admin_service.collect_cash(machine_id)
        if result:
            print(f"Admin: Collected ${result['totalAmount']:.2f}")

    def display_inventory_status(self, machine_id: int):
        products = self.vending_machine_service.get_available_products(machine_id)
        print(f"=== Inventory Status for Machine {machine_id} ===")
        for p in products:
            print(f"  - {p.name} | Price: ${p.price:.2f}")
        print("==========================================")

    def get_sales_report(self, machine_id: int):
        report = self.admin_service.get_sales_report(machine_id)
        print(f"=== Sales Report for Machine {machine_id} ===")
        print(f"  Total Sales: ${report['totalSales']:.2f}")
        print(f"  Total Transactions: {int(report['transactionCount'])}")
        print("==========================================")

    def display_admin_help(self):
        print("=== Admin Help ===")
        print("  1. restockProduct")
        print("  2. collect_cash")
        print("  3. get_sales_report")
        print("==================")
