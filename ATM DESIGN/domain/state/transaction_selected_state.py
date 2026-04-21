from typing import Optional, Dict, TYPE_CHECKING
from domain.exception.invalid_atm_operation import InvalidATMOperationException
from domain.state.abstract_atm_state import AbstractATMState
from domain.state.support_notes import SupportsNotes
from domain.transaction_status import TransactionStatus
from domain.transaction_type import TransactionType
from domain.denomination import Denomination
from domain.state.ATMstate import ATMState

if TYPE_CHECKING:
    from domain.atm import ATM


class TransactionSelectedState(AbstractATMState, SupportsNotes):
    def insertCard(self, atm: 'ATM', cardId: str) -> None:
        raise InvalidATMOperationException("Card already inserted")

    def ejectCard(self, atm: 'ATM') -> None:
        print("[TransactionSelectedState] ejectCard")
        from domain.state.idle_state import IdleState
        atm.setCurrentState(IdleState())

    def enterPin(self, atm: 'ATM', pin: str) -> None:
        raise InvalidATMOperationException("Already authenticated")

    def selectTransaction(self, atm: 'ATM', type: TransactionType) -> None:
        print(f"[TransactionSelectedState] update transaction: {type.name}")
        if atm.getCurrentSession() is not None:
            atm.getCurrentSession().setTransactionType(type)

    def processTransaction(self, atm: 'ATM', amount: int) -> None:
        transactionService = atm.getTransactionService()

        if (
            transactionService is None
            or atm.getCurrentSession() is None
            or not atm.getCurrentSession().transactionTypePresent()
        ):
            raise InvalidATMOperationException("Transaction not initialized")

        session = atm.getCurrentSession()
        transactionType = session.getTransactionType()

        print(f"[TransactionSelectedState] process: type={transactionType.name}, amount={amount}")

        transaction_map = {
            TransactionType.BALANCE: lambda: transactionService.showBalance(session.getId()),
            TransactionType.WITHDRAW: lambda: transactionService.withdrawCash(session.getId(), amount),
            TransactionType.DEPOSIT: lambda: transactionService.depositCash(session.getId(), {}),
        }

        transaction_func = transaction_map.get(transactionType)

        if not transaction_func:
            raise InvalidATMOperationException("Unsupported transaction type")

        transaction = transaction_func()
        atm.setLastTransaction(transaction)

    def processTransactionWithNotes(self, atm: 'ATM', amount: int, notes: Dict[Denomination, int]) -> None:
        transactionService = atm.getTransactionService()
        if transactionService is None or atm.getCurrentSession() is None or not atm.getCurrentSession().transactionTypePresent():
            raise InvalidATMOperationException("Transaction not initialized")
        transactionType = atm.getCurrentSession().getTransactionType()
        print(f"[TransactionSelectedState] process with notes: type={transactionType.name}, amount={amount}")
        if transactionType == TransactionType.DEPOSIT:
            transaction = transactionService.depositCash(atm.getCurrentSession().getId(), notes)
        else:
            self.processTransaction(atm, amount)
            return
        atm.setLastTransaction(transaction)

    def endSession(self, atm: 'ATM') -> None:
        print("[TransactionSelectedState] endSession")
        from domain.state.idle_state import IdleState
        atm.setCurrentState(IdleState())

    def next(self, atm: 'ATM') -> Optional[ATMState]:
        if atm.getLastTransaction() is not None and atm.getLastTransaction().getStatus() == TransactionStatus.SUCCESS:
            from domain.state.transaction_completed_state import TransactionCompletedState
            return TransactionCompletedState()
        if atm.getCurrentSession() is None:
            from domain.state.idle_state import IdleState
            return IdleState()
        return None
