


from typing import TYPE_CHECKING, Dict, Optional, Tuple

from domain.cash_box import CashBox
from domain.denomination import Denomination
from domain.product import Product



if TYPE_CHECKING:
    from domain.state.vending_machine_state import VendingMachineState
    from domain.transaction import Transaction
    from domain.payment_request import PaymentRequest

class VendingMachine:
    def __init__(self,id:int , location:str):
        from domain.state.idle_state import IdleState
        self.id = id
        self.location = location
        self.current_state : VendingMachineState = IdleState()

        self.current_transaction : Optional[Transaction] = None
        self.inventory: Dict[int, Tuple[Product, int]] = {}
        self.cash_box = CashBox(1,id)
        self.operational = True

    def set_state(self, new_state: 'VendingMachineState'):
        self.current_state = new_state
        print(f"Machine {self.id} state changed to: {new_state.state_name}")

    def process_payment(self, request: 'PaymentRequest') -> 'Transaction':
        return self.current_state.process_payment(self, request)

    def cancel_payment(self, transaction_id: int):
        self.current_state.cancel_payment(self, transaction_id)

    @property
    def state_name(self) -> str:
        return self.current_state.state_name

    def add_product(self, product: Product, quantity: int):
        if product.id in self.inventory:
            p, q = self.inventory[product.id]
            self.inventory[product.id] = (p, q + quantity)
        else:
            self.inventory[product.id] = (product, quantity)
        print(f"Added {quantity} units of {product.name} to machine {self.id}")

    def has_product(self, product_id: int) -> bool:
        return product_id in self.inventory and self.inventory[product_id][1] > 0

    def dispense_product(self, product_id: int):
        if self.has_product(product_id):
            product, quantity = self.inventory[product_id]
            self.inventory[product_id] = (product, quantity - 1)
            print(f"Dispensed {product.name} from machine {self.id}")
        else:
            print(f"Cannot dispense product {product_id} - out of stock in machine {self.id}")

    def add_cash(self, denomination: Denomination, count: int):
        self.cash_box.add_denomination(denomination, count)
        print(f"Added {count} {denomination} notes to machine {self.id}")

    def remove_cash(self, denomination: Denomination, count: int) -> bool:
        return self.cash_box.remove_denomination(denomination, count)

    def __str__(self):
        return f"VendingMachine {self.id} at {self.location} - Status: {'Operational' if self.operational else 'Down'}"
