from domain.payment_gateways import PaymentGateWays
from domain.payment_methods import PaymentMethod
from service.template.payment_gateway import PaymentGateway


class PaytmGateway(PaymentGateway):

    def __init__(self):
        self.name = PaymentGateWays.PAYTM

    def create_order(self, payment):
        print(f"[{self.name}] Creating order for {payment.payment_id}")

    def authorize(self, payment):
        print(f"[{self.name}] Authorizing payment {payment.payment_id}")

    def capture(self, payment):
        print(f"[{self.name}] Capturing payment {payment.payment_id}")

    def verify_webhook(self, payload, signature) -> bool:
        print("[{self.name}] Verifying checksum/signature")
        return True

    def supports(self, method):
        return method in {
            PaymentMethod.UPI,
            PaymentMethod.NET_BANKING
        }