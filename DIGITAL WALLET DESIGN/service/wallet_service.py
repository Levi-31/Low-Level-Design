


import time
import uuid

from domain.wallet import Wallet
from domain.wallet_status import WalletStatus
from repository.wallet_repository import WalletRepository


class WalletService:
    def __init__(self, wallet_repository: WalletRepository):
        self._wallet_repository = wallet_repository

    @staticmethod
    def _now_ms() -> int:
        return int(time.time() * 1000)
    
    def create_wallet(self, user_id: str) -> Wallet:
        wallet_id = str(uuid.uuid4())
        account_number = "ACC_" + wallet_id[:8]
        now = self._now_ms()
        wallet = Wallet(wallet_id, account_number, 0, user_id, WalletStatus.ACTIVE, now, now)
        return self._wallet_repository.save(wallet)
    
    def get_by_account_number(self, account_number:str) -> Wallet:
        return self._wallet_repository.find_by_account_number(account_number)
    

    def suspend_wallet(self,account_number:str) -> Wallet:
        wallet_instance = self._wallet_repository.find_by_account_number(account_number)
        if isinstance(wallet_instance , Wallet) and wallet_instance.status == WalletStatus.ACTIVE:
            wallet_instance.status = WalletStatus.SUSPENDED
            self._wallet_repository.save(wallet_instance)
            return wallet_instance
        
        raise Exception("Wallet Does not Exist")
    
    def close_wallet(self, account_number:str) ->Wallet:
        wallet_instance = self._wallet_repository.find_by_account_number(account_number)
        if isinstance(wallet_instance , Wallet) and wallet_instance.status in [WalletStatus.ACTIVE, WalletStatus.SUSPENDED] :
            wallet_instance.status = WalletStatus.CLOSED
            self._wallet_repository.save(wallet_instance)
            return wallet_instance
        raise Exception("Wallet Does not Exist")
    
    def reopen_wallet(self, account_number:str) -> Wallet:
        wallet_instance = self._wallet_repository.find_by_account_number(account_number)
        if isinstance(wallet_instance , Wallet) and wallet_instance.status in [WalletStatus.CLOSED, WalletStatus.SUSPENDED] :
            wallet_instance.status = WalletStatus.ACTIVE
            self._wallet_repository.save(wallet_instance)
            return wallet_instance
        raise Exception("Wallet Does not Exist")
        