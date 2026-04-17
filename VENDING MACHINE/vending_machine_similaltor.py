import sys
import os
import time

from domain.prodcut_category import ProductCategory

# Add current directory to path so imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from domain.denomination import Denomination
from domain.product import Product
from domain.vending_machine import VendingMachine
from domain.payment_request import PaymentRequest
from repository.vending_machine_repository import VendingMachineRepository
from repository.product_repository import ProductRepository
from repository.payment_repository import PaymentRepository
from repository.recovery_repository import RecoveryRepository
from service.vending_machine_service import VendingMachineService
from service.payment_service import PaymentService
from service.recovery_service import RecoveryService
from service.admin_service import AdminService
from controller.vending_machine_controller import VendingMachineController
from controller.payment_controller import PaymentController
from controller.recovery_controller import RecoveryController
from controller.admin_controller import AdminController

def main():
    import pdb;pdb.set_trace()
    print("=== Vending Machine System Simulation (Python) ===")

    # Initialize repositories
    vm_repo = VendingMachineRepository()
    prod_repo = ProductRepository()
    pay_repo = PaymentRepository()
    rec_repo = RecoveryRepository()

    # Initialize services
    vm_service = VendingMachineService(vm_repo, prod_repo)
    pay_service = PaymentService(vm_repo, pay_repo)
    rec_service = RecoveryService(vm_repo, rec_repo, pay_repo)
    admin_service = AdminService(vm_repo, prod_repo, pay_repo)

    # Initialize controllers
    vm_controller = VendingMachineController(vm_service)
    pay_controller = PaymentController(pay_service)
    rec_controller = RecoveryController(rec_service)
    admin_controller = AdminController(admin_service, vm_service)

    # 1. Create a vending machine
    print("\n--- Creating Vending Machine ---")
    machine = VendingMachine(1, "Main Lobby")
    vm_repo.save(machine)

    # 2. Demonstrate system startup recovery
    print("\n--- System Startup Recovery Check ---")
    rec_controller.check_and_recover_all()

    # 3. Add products
    print("\n--- Adding Products to Inventory ---")
    cola = Product(1, "Cola", 2.50, ProductCategory.BEVERAGE)
    chips = Product(2, "Chips", 1.50, ProductCategory.CHIPS)
    chocolate = Product(3, "Chocolate", 1.00, ProductCategory.CANDY)

    prod_repo.save(cola)
    prod_repo.save(chips)
    prod_repo.save(chocolate)

    machine.add_product(cola, 10)
    machine.add_product(chips, 15)
    machine.add_product(chocolate, 20)

    # 4. Display available products
    print("\n--- Available Products ---")
    products = vm_controller.get_available_products(1)
    for p in products:
        print(f"  - {p.name} | ${p.price:.2f}")

    # 5. Process a payment
    print("\n--- Processing Payment ---")
    payment = {Denomination.FIVE_DOLLAR: 1}

    payment_request = PaymentRequest(1, 1, payment)
    transaction = pay_controller.process_payment(1, payment_request)

    if transaction:
        print("✓ Payment processed successfully")
        print(f"  Transaction ID: {transaction.id}")
        print(f"  Amount Required: ${transaction.amount_required:.2f}")
        print(f"  Amount Inserted: ${transaction.amount_inserted:.2f}")
        print(f"  Status: {transaction.status}")

    # 6. Display machine state
    print("\n--- Machine State ---")
    print(f"  Current State: {machine.state_name}")

    # Wait for simulation to finish state transitions (Python might need a bit more care with state)
    time.sleep(1.5)
    print(f"  Final State: {machine.state_name}")

    # 7. Admin operations
    print("\n--- Admin Operations ---")
    admin_controller.display_inventory_status(1)
    admin_controller.get_sales_report(1)
    admin_controller.collect_cash(1)

    print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    main()
