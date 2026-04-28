import uuid

from domain.payment_request import PaymentRequest
from domain.payment_response import PaymentResponse
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from service.strategy.payment_strategy import PaymentStrategy


class CreditCardPayment(PaymentStrategy):

    def process_payment(self, payment_request: PaymentRequest, transaction: Transaction) -> PaymentResponse:

        print("[Card] Authorizing payment")

        transaction.gateway_transaction_id = f"card_txn_{uuid.uuid4()}"

        # sync success
        transaction.update_status(TransactionStatus.SUCCESS)

        return PaymentResponse(
            payment_id=transaction.payment_id,
            status=transaction.status,
            amount=payment_request.amount,
            currency=payment_request.currency,
            gateway=payment_request.gateway.name,
            payment_method=payment_request.payment_method.name,
            message="Payment successful",
            transaction_id=transaction.id
        )
    
