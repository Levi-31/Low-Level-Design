from domain.payment_gateways import PaymentGateWays
from domain.payment_methods import PaymentMethod
from service.template.payment_gateway import PaymentGateway


class RazorpayGateway(PaymentGateway):

    def __init__(self):
        self.name = PaymentGateWays.RAZORPAY

    def create_order(self, payment):
        print(f"[Razorpay] Creating order for {payment.payment_id}")

    def authorize(self, payment):
        print(f"[Razorpay] Authorizing payment {payment.payment_id}")

    def capture(self, payment):
        print(f"[Razorpay] Capturing payment {payment.payment_id}")

    def verify_webhook(self, payload, signature) -> bool:
        print("[Razorpay] Verifying webhook signature")
        # simulate verification
        return True

    def supports(self, method):
        return method in {
            PaymentMethod.UPI,
            PaymentMethod.CREDIT_CARD,
            PaymentMethod.NET_BANKING
        }

