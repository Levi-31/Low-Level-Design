


from dataclasses import dataclass, field
import time

from domain.payment_gateways import PaymentGateWays
from domain.payment_methods import PaymentMethod
from domain.transaction_status import TransactionStatus


@dataclass
class Transaction:
    id: str
    payment_id: str

    gateway: PaymentGateWays
    payment_method: PaymentMethod

    status: TransactionStatus

    user_id : int 

    request_id : str 

    gateway_transaction_id: str = None  # from Razorpay/Paytm

    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


    def update_status(self, new_status: TransactionStatus):
        self.status = new_status
        self.updated_at = time.time()
