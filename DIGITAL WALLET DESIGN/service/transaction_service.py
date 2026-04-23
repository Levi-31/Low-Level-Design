


import time
from typing import Dict, Optional
import uuid

from domain.account_statement import AccountStatement
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from domain.transaction_type import TransactionType
from domain.wallet_status import WalletStatus
from repository.transaction_repository import TransactionRepository
from repository.wallet_repository import WalletRepository
from service.gateway.payment_gateway_router import PaymentGatewayRouter
from service.lock_service import LockService
from service.notification.notification_message import NotificationMessage
from service.notification.notification_router import NotificationRouter


class TransactionService:
    def __init__(self,
                 transaction_repository: TransactionRepository,
                 wallet_repository: WalletRepository,
                 lock_service: LockService,
                 payment_gateway_router: PaymentGatewayRouter,
                 notification_router: NotificationRouter):
        self._transaction_repository = transaction_repository
        self._wallet_repository = wallet_repository
        self._lock_service = lock_service
        self._payment_gateway_router = payment_gateway_router
        self._notification_router = notification_router

    @staticmethod
    def _now_ms() -> int:
        return int(time.time() * 1000)

    @staticmethod
    def _generate_id() -> str:
        return str(uuid.uuid4())
    
    def _get_active_wallet_or_throw(self, account_number: str):
        wallet = self._wallet_repository.find_by_account_number(account_number)
        if wallet is None:
            raise ValueError(f"Wallet not found for account: {account_number}")
        if wallet.status != WalletStatus.ACTIVE:
            raise RuntimeError(f"Wallet is not ACTIVE: {wallet.status.name}")
        return wallet

    def _get_active_or_closed_wallet(self, account_number: str):
        wallet = self._wallet_repository.find_by_account_number(account_number)
        if wallet is None:
            raise ValueError(f"Wallet not found for account: {account_number}")
        return wallet

    def get_statement(self, account_number: str, start_utc: Optional[int],end_utc: Optional[int]) -> AccountStatement:
        wallet = self._get_active_or_closed_wallet(account_number)
        start = start_utc if start_utc is not None else 0
        end   = end_utc   if end_utc   is not None else (2**63 - 1)
        txs = self._transaction_repository.find_by_wallet_and_range(wallet.id, start, end)
        return AccountStatement(wallet.id, wallet.account_number, txs,
                                start_utc, end_utc, wallet.balance_minor)
    
    def initiate_deposit(self, account_number: str, amount_minor: int,payment_method: str, payment_gateway: str,payment_details: Dict[str, str]) -> Transaction:
        if amount_minor <= 0:
            raise ValueError("Amount must be positive (minor units)")
        wallet = self._get_active_wallet_or_throw(account_number)

        selected = self._payment_gateway_router.select_provider(
            payment_gateway, amount_minor, "CRYPTOOOOOOO")
        provider = self._payment_gateway_router.resolve(selected)
        provider_ref = provider.initiate_payment(
            account_number, amount_minor, payment_method, payment_details)

        tx = Transaction(
            self._generate_id(),
            "",
            wallet.id,
            amount_minor,
            TransactionType.DEPOSIT,
            TransactionStatus.PENDING,
            provider_ref,
            f"Deposit via {selected}",
            self._now_ms()
        )
        return self._transaction_repository.save(tx)

    def transfer(self, from_account_number: str, to_account_number: str,amount_minor: int, description: str) -> Transaction:

        if not from_account_number or not to_account_number:
            raise ValueError("Account numbers cannot be null")
        if from_account_number == to_account_number:
            raise ValueError("Cannot transfer to the same account")
        if amount_minor <= 0:
            raise ValueError("Amount must be positive (minor units)")

        from_wallet = self._get_active_wallet_or_throw(from_account_number)
        to_wallet   = self._get_active_wallet_or_throw(to_account_number)

        lock_key1 = "wallet_lock_" + from_wallet.id
        lock_key2 = "wallet_lock_" + to_wallet.id

        # Sort keys to avoid deadlocks
        sorted_keys = sorted([lock_key1, lock_key2])
        first_acquired  = False
        second_acquired = False

        try:
            if self._lock_service.acquire(sorted_keys[0], 5000):
                first_acquired = True
            else:
                raise RuntimeError("Failed to acquire lock")

            if self._lock_service.acquire(sorted_keys[1], 5000):
                second_acquired = True
            else:
                self._lock_service.release(sorted_keys[0])
                first_acquired = False
                raise RuntimeError("Failed to acquire lock")

            # Re-fetch wallets under lock to ensure latest state
            from_wallet = self._wallet_repository.find_by_id(from_wallet.id)
            to_wallet   = self._wallet_repository.find_by_id(to_wallet.id)
            if from_wallet is None:
                raise RuntimeError("Source wallet not found")
            if to_wallet is None:
                raise RuntimeError("Destination wallet not found")

            if (from_wallet.status != WalletStatus.ACTIVE or
                    to_wallet.status != WalletStatus.ACTIVE):
                raise RuntimeError("One or more wallets are not ACTIVE")

            if from_wallet.balance_minor < amount_minor:
                raise RuntimeError("Insufficient balance")

            from_wallet.balance_minor -= amount_minor
            to_wallet.balance_minor   += amount_minor
            from_wallet.updated_at = self._now_ms()
            to_wallet.updated_at   = self._now_ms()
            self._wallet_repository.save(from_wallet)
            self._wallet_repository.save(to_wallet)

            tx = Transaction(
                self._generate_id(),
                from_wallet.id,
                to_wallet.id,
                amount_minor,
                TransactionType.TRANSFER,
                TransactionStatus.COMPLETED,
                "",
                description,
                self._now_ms()
            )
            tx = self._transaction_repository.save(tx)

            # TODO: Populate correct recipient email (lookup from UserRepository if needed)
            self._notification_router.send("email", NotificationMessage(
                "user@example.com",
                "Transfer Completed",
                f"Transfer of {amount_minor} minor units from {from_account_number} "
                f"to {to_account_number} completed."
            ))
            return tx
        finally:
            if second_acquired:
                self._lock_service.release(sorted_keys[1])
            if first_acquired:
                self._lock_service.release(sorted_keys[0])


    def handle_deposit_callback(self, provider_ref: str, status: TransactionStatus):
        tx = self._transaction_repository.find_by_provider_ref(provider_ref)
        if tx is None:
            raise ValueError(f"Transaction not found for providerRef: {provider_ref}")

        if tx.status in (TransactionStatus.COMPLETED, TransactionStatus.FAILED):
            return  # already processed

        wallet_id = tx.to_wallet_id
        lock_key  = "wallet_lock_" + wallet_id
        if not self._lock_service.acquire(lock_key, 5000):
            raise RuntimeError(f"Failed to acquire lock for wallet {wallet_id}")
        try:
            wallet = self._wallet_repository.find_by_id(wallet_id)
            if wallet is None:
                raise RuntimeError("Wallet not found for transaction")

            if status == TransactionStatus.COMPLETED:
                wallet.balance_minor += tx.amount_minor
                wallet.updated_at = self._now_ms()
                self._wallet_repository.save(wallet)
                tx.status = TransactionStatus.COMPLETED

                # TODO: Lookup real email for wallet owner
                self._notification_router.send("email", NotificationMessage(
                    "user@example.com",
                    "Deposit Completed",
                    f"Deposit of {tx.amount_minor} minor units to account credited."
                ))
            else:
                tx.status = TransactionStatus.FAILED
            self._transaction_repository.save(tx)
        finally:
            self._lock_service.release(lock_key)


    def withdraw(self, account_number: str, amount_minor: int, description: str) -> Transaction:
        
        if amount_minor <= 0:
            raise ValueError("Amount must be positive (minor units)")
        wallet = self._get_active_wallet_or_throw(account_number)
        if wallet.balance_minor < amount_minor:
            raise RuntimeError("Insufficient balance")

        # Create PENDING withdrawal; an external payout service would complete it
        tx = Transaction(
            self._generate_id(),
            wallet.id,
            "",
            amount_minor,
            TransactionType.WITHDRAWAL,
            TransactionStatus.PENDING,
            "",
            description,
            self._now_ms()
        )
        tx = self._transaction_repository.save(tx)
        # TODO: Integrate with payout provider
        return tx