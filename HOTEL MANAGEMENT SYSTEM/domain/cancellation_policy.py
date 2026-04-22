


from dataclasses import dataclass

@dataclass
class CancellationPolicy:
    id: str
    name: str
    refund_percent: int
    cutoff_hours_before_check_in: int
    created_at: int