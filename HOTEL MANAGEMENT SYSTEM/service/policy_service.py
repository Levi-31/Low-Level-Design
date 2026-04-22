




from domain.booking import Booking
from domain.cancellation_policy import CancellationPolicy
from domain.refund_decision import RefundDecision


class PolicyService:
    def evaluate_cancellation(self, booking: Booking, policy: CancellationPolicy, now_utc: int) -> RefundDecision:
        hours_until_check_in = (booking.check_in_date_utc - now_utc) / (1000 * 60 * 60)

        if hours_until_check_in < policy.cutoff_hours_before_check_in:
            return RefundDecision(0, 0)
        
        refund_percent = policy.refund_percent
        refund_amount = (booking.total_amount_minor * refund_percent) // 100

        return RefundDecision(refund_percent, refund_amount)
