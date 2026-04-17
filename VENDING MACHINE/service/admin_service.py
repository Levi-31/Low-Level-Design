from typing import Dict, Any, List
from repository.vending_machine_repository import VendingMachineRepository
from repository.product_repository import ProductRepository
from repository.payment_repository import PaymentRepository
from domain.transaction_status import TransactionStatus

class AdminService:
    def __init__(self, vm_repo: VendingMachineRepository, prod_repo: ProductRepository, pay_repo: PaymentRepository):
        self.vending_machine_repository = vm_repo
        self.product_repository = prod_repo
        self.payment_repository = pay_repo
        print("AdminService initialized")

    def restock_product(self, machine_id: int, product_id: int, quantity: int):
        machine = self.vending_machine_repository.find_by_id(machine_id)
        product = self.product_repository.find_by_id(product_id)
        if machine and product:
            machine.add_product(product, quantity)

    def collect_cash(self, machine_id: int) -> Dict[str, float]:
        print(f"AdminService: Collecting cash from machine {machine_id}")
        machine = self.vending_machine_repository.find_by_id(machine_id)
        return {"totalAmount": machine.cash_box.total_amount} if machine else {}

    def get_sales_report(self, machine_id: int) -> Dict[str, float]:
        transactions = self.payment_repository.find_all_by_machine_id(machine_id)
        total_sales = sum(t.amount_required for t in transactions if t.status == TransactionStatus.COMPLETED)
        count = sum(1 for t in transactions if t.status == TransactionStatus.COMPLETED)
        return {"totalSales": total_sales, "transactionCount": float(count)}
