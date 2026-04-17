


import time

from domain.transaction_status import TransactionStatus


class Transaction:
    def __init__(self,id:int,vending_machine_id:int, product_id :int, amount_required:float):
        self.id = id
        self.vending_machine_id = vending_machine_id
        self.product_id = product_id
        self.amount_required = amount_required
        self.amount_inserted = 0.0
        self.change_returned = 0.0
        self.status = TransactionStatus.PENDING
        self.timestamp = int(time.time() * 1000)

    def is_payment_complete(self) -> bool:
        return self.amount_inserted >= self.amount_required

    def get_remaining_amount(self) -> float:
        return max(0.0, self.amount_required - self.amount_inserted)

    def add_payment(self, amount: float):
        self.amount_inserted += amount
        if self.is_payment_complete():
            self.status = TransactionStatus.COMPLETED

    def cancel(self):
        self.status = TransactionStatus.CANCELLED

    def fail(self):
        self.status = TransactionStatus.FAILED

    def __str__(self):
        return f"Transaction {self.id} - Product: {self.product_id}, Status: {self.status}, Amount: ${self.amount_required:.2f}"