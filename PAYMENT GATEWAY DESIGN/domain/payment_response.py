


from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentResponse:
    payment_id: str
    status: str

    amount: float
    currency: str

    gateway: str
    payment_method: str

    message: Optional[str] = None

    # useful for client tracking
    transaction_id: Optional[str] = None