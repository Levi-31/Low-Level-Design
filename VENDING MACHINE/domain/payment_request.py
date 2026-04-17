from typing import Dict
from domain.denomination import Denomination

class PaymentRequest:
    def __init__(self, product_id: int, quantity: int, denominations: Dict[Denomination, int]):
        self.product_id = product_id
        self.quantity = quantity
        self.denominations = denominations
        self.total_amount = sum(denom.value_in_dollars * count for denom, count in denominations.items())

    def __str__(self):
        return f"PaymentRequest - Product: {self.product_id}, Amount: ${self.total_amount:.2f}"
