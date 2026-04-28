from enum import Enum

from domain.payment_gateways import PaymentGateWays
from domain.payment_methods import PaymentMethod
from service.strategy.credit_card_payment_strategy import CreditCardPayment
from service.strategy.net_banking_payment_strategy import NetBankingPayment
from service.strategy.payment_strategy import PaymentStrategy
from service.strategy.upi_payment_strategy import UPIPayment
from service.template.payment_gateway import PaymentGateway
from service.template.paytm_gateway import PaytmGateway
from service.template.razorpay_payment_gateway import RazorpayGateway


class PaymentFactory:
    @staticmethod
    def get_gateway(name:Enum) -> PaymentGateway :
        gateway_map = {
            PaymentGateWays.RAZORPAY : RazorpayGateway,
            PaymentGateWays.PAYTM : PaytmGateway
        }

        gateway_class = gateway_map.get(name)
        if gateway_class:
            return gateway_class()
        
        raise ValueError("Invalid gateway")
        
    

    @staticmethod
    def get_payment_strategy(payment_method:Enum, gateway:PaymentGateway) -> PaymentStrategy:

        payment_method_map = {
            PaymentMethod.UPI : UPIPayment,
            PaymentMethod.NET_BANKING : NetBankingPayment,
            PaymentMethod.CREDIT_CARD : CreditCardPayment
        }

        strategy_cls = payment_method_map.get(payment_method)

        if strategy_cls:
            return strategy_cls(gateway)
        
        raise ValueError("Invalid method")

