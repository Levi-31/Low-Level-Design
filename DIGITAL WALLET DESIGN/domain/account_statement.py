

from typing import List, Optional

from domain.transaction import Transaction


class AccountStatement:
    def __init__(self, wallet_id: str, wallet_account_number: str,
                 transactions: List[Transaction],
                 start_date_utc: Optional[int], end_date_utc: Optional[int],
                 current_balance_minor: int):
        self._wallet_id = wallet_id
        self._wallet_account_number = wallet_account_number
        self._transactions = transactions
        self._start_date_utc = start_date_utc
        self._end_date_utc = end_date_utc
        self._current_balance_minor = current_balance_minor
    

    @property
    def wallet_id(self) -> str:
        return self._wallet_id

    @wallet_id.setter
    def wallet_id(self, value: str):
        self._wallet_id = value

    @property
    def wallet_account_number(self) -> str:
        return self._wallet_account_number

    @wallet_account_number.setter
    def wallet_account_number(self, value: str):
        self._wallet_account_number = value

    @property
    def transactions(self) -> List[Transaction]:
        return self._transactions

    @transactions.setter
    def transactions(self, value: List[Transaction]):
        self._transactions = value

    @property
    def start_date_utc(self) -> Optional[int]:
        return self._start_date_utc

    @start_date_utc.setter
    def start_date_utc(self, value: Optional[int]):
        self._start_date_utc = value

    @property
    def end_date_utc(self) -> Optional[int]:
        return self._end_date_utc

    @end_date_utc.setter
    def end_date_utc(self, value: Optional[int]):
        self._end_date_utc = value

    @property
    def current_balance_minor(self) -> int:
        return self._current_balance_minor

    @current_balance_minor.setter
    def current_balance_minor(self, value: int):
        self._current_balance_minor = value