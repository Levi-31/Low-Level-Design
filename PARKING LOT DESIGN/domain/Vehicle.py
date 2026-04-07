from enum import Enum
import uuid


class Vehicle:
    class VehicleType(Enum):
        BIKE = "BIKE"
        CAR = "CAR"
        TRUCK = "TRUCK"
        EV = "EV"

        
    def __init__(self, vehicle_number: str,vehicle_type : VehicleType):
        self.id = str(uuid.uuid4())
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type

    def __str__(self):
        return f"Vehicle(id={self.id}, license_plate='{self.vehicle_number}', type={self.vehicle_type.value})"

