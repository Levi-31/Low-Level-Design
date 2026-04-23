


from typing import Optional, Dict
from domain.wallet import Wallet
from repository.wallet_repository import WalletRepository


class WalletRepositoryImpl(WalletRepository):
    def __init__(self):
        self._wallets_by_id: Dict[str, Wallet] = {}
        self._wallet_id_by_account_number: Dict[str, str] = {}

    def save(self, wallet: Wallet) -> Wallet:
        self._wallets_by_id[wallet.id] = wallet
        self._wallet_id_by_account_number[wallet.account_number] = wallet.id
        return wallet

    def find_by_id(self, wallet_id: str) -> Optional[Wallet]:
        return self._wallets_by_id.get(wallet_id)

    def find_by_account_number(self, account_number: str) -> Optional[Wallet]:
        wallet_id = self._wallet_id_by_account_number.get(account_number)
        if wallet_id is None:
            return None
        return self._wallets_by_id.get(wallet_id)