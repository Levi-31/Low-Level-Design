

from abc import ABC, abstractmethod
from typing import Optional
from domain.wallet import Wallet


class WalletRepository(ABC):
    @abstractmethod
    def save(self, wallet: Wallet) -> Wallet:
        pass

    @abstractmethod
    def find_by_id(self, wallet_id: str) -> Optional[Wallet]:
        pass

    @abstractmethod
    def find_by_account_number(self, account_number: str) -> Optional[Wallet]:
        pass