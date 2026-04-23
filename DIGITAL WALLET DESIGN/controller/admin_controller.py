



from domain.wallet import Wallet
from service.wallet_service import WalletService


class AdminController:
    def __init__(self, wallet_service: WalletService):
        self._wallet_service = wallet_service

    def suspend_wallet(self, account_number: str) -> Wallet:
        return self._wallet_service.suspend_wallet(account_number)

    def close_wallet(self, account_number: str) -> Wallet:
        return self._wallet_service.close_wallet(account_number)

    def reopen_wallet(self, account_number: str) -> Wallet:
        return self._wallet_service.reopen_wallet(account_number)