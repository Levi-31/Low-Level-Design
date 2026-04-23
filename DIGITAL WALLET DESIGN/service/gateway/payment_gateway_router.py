

from typing import Dict

from service.gateway.payment_gateway_provider import PaymentGatewayProvider


class PaymentGatewayRouter:
    def __init__(self):
        self._providers: Dict[str, PaymentGatewayProvider] = {}

    def register(self, provider: PaymentGatewayProvider):
        self._providers[provider.get_name().lower()] = provider

    def select_provider(self, preferred_gateway: str, amount_minor: int, currency: str) -> str:
        """Prefer requested gateway; fall back to any registered one."""
        if preferred_gateway:
            key = preferred_gateway.lower()
            if key in self._providers:
                return key
        if self._providers:
            return next(iter(self._providers))
        raise RuntimeError("No payment providers registered")
    
    def resolve(self, gateway_name: str) -> PaymentGatewayProvider:
        key = gateway_name.lower()
        provider = self._providers.get(key)
        if provider is None:
            raise ValueError(f"Payment provider not registered: {gateway_name}")
        return provider