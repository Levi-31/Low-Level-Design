import uuid

from domain.payment_request import PaymentRequest
from domain.payment_response import PaymentResponse
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus
from service.strategy.payment_strategy import PaymentStrategy


class UPIPayment(PaymentStrategy):


    def process_payment(self, payment_request:PaymentRequest, transaction:Transaction)-> PaymentResponse:
        print(f"[UPI] Initiating payment for user {payment_request.user_id}")
        print("[UPI] Creating collect request")

        print("[UPI] Sending request to PSP")

        transaction.gateway_transaction_id = f"upi_txn_{uuid.uuid4()}"

        transaction.update_status(TransactionStatus.PENDING)


        print("[UPI] Waiting for user approval (callback expected)")

        return PaymentResponse(
            payment_id=transaction.payment_id,
            status=transaction.status,
            amount=payment_request.amount,
            currency=payment_request.currency,
            gateway=payment_request.gateway.name,
            payment_method=payment_request.payment_method.name,
            message="UPI collect request sent",
            transaction_id=transaction.id
        )
    



