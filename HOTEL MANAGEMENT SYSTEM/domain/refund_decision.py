


from dataclasses import dataclass

@dataclass
class RefundDecision:
    refund_percent: int
    refund_amount_minor: int