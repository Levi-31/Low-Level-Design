import uuid

from domain.payment_request import PaymentRequest
from domain.payment_response import PaymentResponse
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from service.strategy.payment_strategy import PaymentStrategy


class NetBankingPayment(PaymentStrategy):

    def process_payment(self, payment_request:PaymentRequest, transaction:Transaction)-> PaymentResponse:
        print(f"[NetBanking] Initiating payment for user {payment_request.user_id}")
        print("[NetBanking] Creating order with gateway")

        # simulate redirect
        redirect_url = "https://bank.com/auth"

        transaction.update_status(TransactionStatus.PENDING)
        transaction.gateway_transaction_id = f"NetBank_{uuid.uuid4()}"

        print("[NetBanking] Redirecting user to bank page")

        return PaymentResponse(
            payment_id=transaction.payment_id,
            status=transaction.status,
            amount=payment_request.amount,
            currency=payment_request.currency,
            gateway=payment_request.gateway.name,
            payment_method=payment_request.payment_method.name,
            message="Redirect user to bank",
            redirect_url=redirect_url,
            transaction_id=transaction.id
        )
    

