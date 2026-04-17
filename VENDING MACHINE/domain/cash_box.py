
from typing import Dict

from domain.denomination import Denomination


class CashBox:
    def __init__(self,id:int, vending_machine_id:int):
        self.id = id
        self.vending_machine_id = vending_machine_id

        self.denominations: Dict[Denomination, int] = {}
        self.total_amount: float = 0.0
        self._initialize_cash_box()

    
    def _initialize_cash_box(self):
        self.denominations = {
            Denomination.ONE_DOLLAR: 10,
            Denomination.FIVE_DOLLAR: 5,
            Denomination.TEN_DOLLAR: 3,
            Denomination.TWENTY_DOLLAR: 2,
            Denomination.FIFTY_DOLLAR: 1,
            Denomination.HUNDRED_DOLLAR: 1
        }
        self._calculate_total_amount()
    

    def _calculate_total_amount(self):
        self.total_amount = sum(denom.value_in_dollars * count for denom, count in self.denominations.items())

    def add_denomination(self, denomination: Denomination, count: int):
        self.denominations[denomination] = self.denominations.get(denomination, 0) + count
        self._calculate_total_amount()

    def remove_denomination(self, denomination: Denomination, count: int) -> bool:
        if self.denominations.get(denomination, 0) >= count:
            self.denominations[denomination] -= count
            self._calculate_total_amount()
            return True
        return False
    
    def has_sufficient_change(self, amount: float) -> bool:
        return self.total_amount >= amount
    
    def calculate_change(self, amount: float) -> Dict[Denomination, int]:
        change = {}
        remaining_amount = amount
        sorted_denoms = sorted(Denomination, key=lambda d: d.value, reverse=True)

        for denom in sorted_denoms:
            available_count = self.denominations.get(denom, 0)
            denom_value = denom.value_in_dollars

            if remaining_amount >= denom_value and available_count > 0:
                count_needed = int(remaining_amount / denom_value)
                count_to_use = min(count_needed, available_count)
                
                if count_to_use > 0:
                    change[denom] = count_to_use
                    remaining_amount -= count_to_use * denom_value
                
                if remaining_amount < 0.01:
                    break
        return change

    def __str__(self):
            return f"CashBox {self.id} - Total: ${self.total_amount:.2f}"
