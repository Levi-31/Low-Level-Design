


from dataclasses import dataclass

from domain.transaction_status import TransactionStatus


@dataclass
class Transaction:
    id: str
    booking_id: str
    amount_minor: int
    currency: str
    status: TransactionStatus
    provider_ref: str
    initiated_at: int
    completed_at: int = 0
    refunded_at: int = 0