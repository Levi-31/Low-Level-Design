import uuid

from domain.Vehicle import Vehicle


class PricingRule:
    def __init__(self,vehicle_type:Vehicle.VehicleType,rate_per_hour:float , flat_rate:float):
        self.id = uuid.uuid4()
        self.vehicle_type = vehicle_type
        self.rate_per_hour: float = rate_per_hour
        self.flat_rate : float = flat_rate

    def update_rates(self, rate_per_hour: float, flat_rate: float):
        self.rate_per_hour = rate_per_hour
        self.flat_rate = flat_rate

    def __str__(self):
        return f"PricingRule(type={self.vehicle_type.value}, rate={self.rate_per_hour}, flat={self.flat_rate})"