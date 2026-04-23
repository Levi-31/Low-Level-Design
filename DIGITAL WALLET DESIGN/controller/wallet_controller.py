



from typing import Optional

from domain.account_statement import AccountStatement
from domain.wallet import Wallet
from service.transaction_service import TransactionService
from service.wallet_service import WalletService


class WalletController:
    def __init__(self, wallet_service: WalletService,
                 transaction_service: TransactionService):
        self._wallet_service = wallet_service
        self._transaction_service = transaction_service

    def create_wallet(self, user_id: str) -> Wallet:
        return self._wallet_service.create_wallet(user_id)

    def get_balance(self, account_number: str) -> int:
        wallet =  self._wallet_service.get_by_account_number(account_number)
        if isinstance(wallet , Wallet):
            return wallet.balance_minor

        return None

    def get_statement(self, account_number: str, start_utc: Optional[int],end_utc: Optional[int]) -> AccountStatement:
        return self._transaction_service.get_statement(account_number, start_utc, end_utc)