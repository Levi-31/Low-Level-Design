


from dataclasses import dataclass

from domain.payment_gateways import PaymentGateWays
from domain.payment_methods import PaymentMethod


from dataclasses import dataclass

@dataclass
class PaymentRequest:
    sender: str
    receiver: str
    amount: float
    currency: str
    gateway: PaymentGateWays
    payment_method: PaymentMethod
    user_id : int
    request_id : str

