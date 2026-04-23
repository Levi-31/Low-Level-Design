



import time
import uuid

from controller.admin_controller import AdminController
from controller.transaction_controller import TransactionController
from controller.wallet_controller import WalletController
from domain.transaction_status import TransactionStatus
from domain.user import User
from repository.implementation.transaction_repository_implementation import TransactionRepositoryImpl
from repository.implementation.user_repository_implementation import UserRepositoryImpl
from repository.implementation.wallet_repository_implementation import WalletRepositoryImpl
from service.gateway.mock_payment_gateway import MockPaymentGatewayProvider
from service.gateway.payment_gateway_router import PaymentGatewayRouter
from service.lock_service import LockService
from service.notification.email_notification_channel import EmailNotificationChannel
from service.notification.notification_router import NotificationRouter
from service.notification.sms_notification_channel import SmsNotificationChannel
from service.transaction_service import TransactionService
from service.wallet_service import WalletService


def now_ms() -> int:
    return int(time.time() * 1000)


def main():
    print("=== DIGITAL WALLET SYSTEM SIMULATION ===\n")

    # Initialize repositories
    user_repository        = UserRepositoryImpl()
    wallet_repository      = WalletRepositoryImpl()
    transaction_repository = TransactionRepositoryImpl()

    # Initialize infrastructure services
    lock_service = LockService()  # TODO: Replace with Redis-based distributed lock

    payment_gateway_router = PaymentGatewayRouter()
    payment_gateway_router.register(MockPaymentGatewayProvider())  # TODO: Register real PG provider(s)

    notification_router = NotificationRouter()
    notification_router.register_channel("email", EmailNotificationChannel())  # TODO: Replace with real email provider
    notification_router.register_channel("sms",   SmsNotificationChannel())   # TODO: Replace with Twilio

    # Initialize domain services
    wallet_service = WalletService(wallet_repository)
    transaction_service = TransactionService(
        transaction_repository, wallet_repository, lock_service,
        payment_gateway_router, notification_router)

    # Initialize controllers
    wallet_controller      = WalletController(wallet_service, transaction_service)
    transaction_controller = TransactionController(transaction_service)
    admin_controller       = AdminController(wallet_service)

    # -----------------------------------------------------------------------
    # Simulation flow
    # -----------------------------------------------------------------------

    import pdb;pdb.set_trace()

    
    print("1. Creating users...")
    user_a = User(str(uuid.uuid4()), "alice", "alice@example.com", "Alice", now_ms())
    user_repository.save(user_a)
    user_b = User(str(uuid.uuid4()), "bob", "bob@example.com", "Bob", now_ms())
    user_repository.save(user_b)
    print(f"Users created: {user_a} | {user_b}")

    print("\n2. Creating wallets...")
    wallet_a = wallet_controller.create_wallet(user_a.id)
    wallet_b = wallet_controller.create_wallet(user_b.id)
    print(f"Wallet A: {wallet_a}")
    print(f"Wallet B: {wallet_b}")

    print("\n3. Initiating deposit for Wallet A...")
    payment_details = {}  # TODO: populate card/UPI details as needed
    dep_tx = transaction_controller.initiate_deposit(
        wallet_a.account_number, 50000, "CARD", "mock", payment_details)
    print(f"Deposit initiated: {dep_tx}")

    print("\n4. Simulating payment success callback...")
    transaction_controller.handle_payment_callback(dep_tx.provider_ref, TransactionStatus.COMPLETED)
    print(f"Deposit completed. Balance A: {wallet_controller.get_balance(wallet_a.account_number)}")

    print("\n5. Transfer from Wallet A to Wallet B...")
    transfer_tx = transaction_controller.transfer(
        wallet_a.account_number, wallet_b.account_number, 20000, "Pay Bob")
    print(f"Transfer completed: {transfer_tx}")
    print(f"Balance A: {wallet_controller.get_balance(wallet_a.account_number)}")
    print(f"Balance B: {wallet_controller.get_balance(wallet_b.account_number)}")

    print("\n6. Withdrawal request from Wallet B...")
    withdraw_tx = transaction_controller.withdraw(
        wallet_b.account_number, 10000, "Withdraw to bank")
    print(f"Withdrawal initiated: {withdraw_tx}")

    print("\n7. Statement for Wallet A...")
    statement_a = wallet_controller.get_statement(wallet_a.account_number, None, None)
    print(f"Statement A: tx count = {len(statement_a.transactions)}, "
          f"balance = {statement_a.current_balance_minor}")

    print("\n8. Suspend Wallet B...")
    admin_controller.suspend_wallet(wallet_b.account_number)
    print("Wallet B suspended. Trying another transfer (should fail)...")
    try:
        transaction_controller.transfer(
            wallet_a.account_number, wallet_b.account_number, 1000, "Test after suspend")
    except Exception as ex:
        print(f"Expected failure: {ex}")

    print("\n=== SIMULATION COMPLETED ===")


if __name__ == "__main__":
    main()
