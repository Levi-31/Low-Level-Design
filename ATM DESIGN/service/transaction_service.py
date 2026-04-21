from typing import Dict, Optional

from domain.denomination import Denomination
from domain.strategy.balance_enquiry_strategy import BalanceInquiryStrategy
from domain.strategy.deposit_strategy import DepositStrategy
from domain.strategy.transaction_strategy import TransactionStrategy
from domain.strategy.withdrawal_strategy import WithdrawalStrategy
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from domain.transaction_type import TransactionType
from repository.transaction_repository import TransactionRepositoryImpl


class TransactionService:
    def __init__(self, transactionRepository: TransactionRepositoryImpl) -> None:
        self.transactionRepository = transactionRepository
        self.strategies: Dict[TransactionType, TransactionStrategy] = {
            TransactionType.WITHDRAW: WithdrawalStrategy(),
            TransactionType.DEPOSIT: DepositStrategy(),
            TransactionType.BALANCE: BalanceInquiryStrategy(),
        }

    def showBalance(self, sessionId: str) -> Transaction:
        return self.processTransaction(sessionId, 0, {}, TransactionType.BALANCE)

    def withdrawCash(self, sessionId: str, amountMinorUnits: int) -> Transaction:
        return self.processTransaction(sessionId, amountMinorUnits, {}, TransactionType.WITHDRAW)

    def depositCash(self, sessionId: str, notes: Dict[Denomination, int]) -> Transaction:
        amount = sum(denomination.value * count for denomination, count in notes.items())
        return self.processTransaction(sessionId, amount, notes, TransactionType.DEPOSIT)

    def acknowledgeTransaction(self, transactionId: str) -> None:
        self.transactionRepository.updateTransactionStatus(transactionId, TransactionStatus.SUCCESS)

    def validateTransaction(self, transaction: Transaction) -> bool:
        return True

    def processTransaction(self, sessionId: str, amount: int, notes: Optional[Dict[Denomination, int]], transactionType: TransactionType) -> Transaction:
        strategy = self.strategies[transactionType]
        transaction = strategy.processTransaction(sessionId, amount, notes)
        return self.transactionRepository.save(transaction)
