

from typing import Dict
import uuid

from service.gateway.payment_gateway_provider import PaymentGatewayProvider


class MockPaymentGatewayProvider(PaymentGatewayProvider):
    def get_name(self) -> str:
        return "mock"

    def initiate_payment(self, account_number: str, amount_minor: int,
                         payment_method: str, payment_details: Dict[str, str]) -> str:
        # TODO: Integrate with actual payment gateway
        return "PG_REF_" + str(uuid.uuid4()).replace("-", "")

    def verify_callback(self, provider_ref: str, status: str) -> bool:
        # TODO: Verify signature/callback with PG
        return True