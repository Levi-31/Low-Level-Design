from controller.admin_controller import AdminController
from controller.card_controller import CardController
from controller.session_controller import SessionController
from controller.transaction_controller import TransactionController
from domain.account import Account
from domain.admin_user import AdminUser
from domain.atm import ATM
from domain.card import Card
from domain.cash_drawer import CashDrawer
from domain.denomination import Denomination
from repository.account_repository import AccountRepositoryImpl
from repository.admin_repository import AdminUserRepositoryImpl
from repository.atm_repository import ATMRepositoryImpl
from repository.card_repository import CardRepositoryImpl
from repository.cash_drawer_repository import CashDrawerRepositoryImpl
from repository.session_repository import SessionRepositoryImpl
from repository.transaction_repository import TransactionRepositoryImpl
from service.admin_service import AdminService
from service.atm_service import ATMService
from service.card_service import CardService
from service.session_service import SessionService
from service.transaction_service import TransactionService


def setupTestData(
    atmRepository: ATMRepositoryImpl,
    cardRepository: CardRepositoryImpl,
    accountRepository: AccountRepositoryImpl,
    adminUserRepository: AdminUserRepositoryImpl,
    cashDrawerRepository: CashDrawerRepositoryImpl
) -> None:
    atm = ATM("ATM_001", "Main Street Branch")
    atmRepository.save(atm)
    cashDrawer = CashDrawer("ATM_001")
    cashDrawer.addNotes(Denomination.ONE_HUNDRED, 50)
    cashDrawer.addNotes(Denomination.TWO_HUNDRED, 25)
    cashDrawer.addNotes(Denomination.FIVE_HUNDRED, 10)
    cashDrawerRepository.save(cashDrawer)
    card = Card("CARD_001", "ACC_001", "12/25")
    cardRepository.save(card)
    account = Account("ACC_001", "John Doe", 100000)
    accountRepository.save(account)
    admin = AdminUser("ADMIN_001", "Admin User", "1234")
    adminUserRepository.save(admin)


def main() -> None:
    atmRepository = ATMRepositoryImpl()
    cardRepository = CardRepositoryImpl()
    accountRepository = AccountRepositoryImpl()
    transactionRepository = TransactionRepositoryImpl()
    sessionRepository = SessionRepositoryImpl()
    cashDrawerRepository = CashDrawerRepositoryImpl()
    adminUserRepository = AdminUserRepositoryImpl()

    atmService = ATMService(atmRepository, cashDrawerRepository)
    cardService = CardService(cardRepository)
    sessionService = SessionService(sessionRepository)
    transactionService = TransactionService(transactionRepository)
    adminService = AdminService(adminUserRepository, cashDrawerRepository, transactionRepository)

    cardController = CardController(atmService)
    sessionController = SessionController(sessionService, atmService)
    transactionController = TransactionController(transactionService, sessionService, atmService)
    adminController = AdminController(adminService)

    # Note: Removed pdb trace for smooth test run.
    import pdb;pdb.set_trace()
    setupTestData(atmRepository, cardRepository, accountRepository, adminUserRepository, cashDrawerRepository)

    demoAtm = atmService.getATM("ATM_001")
    if demoAtm is not None:
        demoAtm.attachServices(cardService, sessionService, transactionService)

    print("=== ATM Machine Simulation ===")
    atmId = "ATM_001"
    cardId = "CARD_001"

    print("\n1. Card Operations:")
    cardInserted = cardController.insertCard(atmId, cardId)
    print(f"Card inserted: {cardInserted}")

    print("\n2. Session Management:")
    session = sessionController.startSession(atmId, cardId)
    print(f"Session started: {session.getId() if session is not None else 'N/A'}")

    print("\n3. Authentication:")
    authenticated = cardController.authenticateCard(atmId, cardId, "1234")
    print(f"Authentication: {authenticated}")

    print("\n4. Transaction Operations:")
    balanceTransaction = transactionController.showBalance(session.getId()) if session else None
    print(f"Balance inquiry: {balanceTransaction.getStatus().value if balanceTransaction is not None else 'Failed'}")
    
    withdrawAmount = 10000
    withdrawTransaction = transactionController.withdrawCash(session.getId(), withdrawAmount) if session else None
    print(f"Withdrawal: {withdrawTransaction.getStatus().value if withdrawTransaction is not None else 'Failed'}")
    
    depositNotes = {Denomination.ONE_HUNDRED: 2}
    depositTransaction = transactionController.depositCash(session.getId(), depositNotes) if session else None
    print(f"Deposit: {depositTransaction.getStatus().value if depositTransaction is not None else 'Failed'}")

    print("\n5. Admin Operations:")
    adminLoggedIn = adminController.loginAdmin("ADMIN_001", "1234")
    print(f"Admin login: {adminLoggedIn}")
    if adminLoggedIn:
        cashDrawerAudit = adminController.auditCash(atmId)
        if cashDrawerAudit is not None:
            print(f"Cash audit - Total: ${cashDrawerAudit.getTotalCash() // 100}")
        else:
            print(f"Cash audit - No cash drawer found for ATM: {atmId}")

    if session:
        sessionController.endSession(session.getId())
    cardController.ejectCard(atmId)
    print("Session ended and card ejected")


if __name__ == "__main__":
    main()
