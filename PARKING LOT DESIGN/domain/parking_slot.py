import uuid

from domain.Vehicle import Vehicle



class ParkingSlot:
    def __init__(self,slot_type:Vehicle.VehicleType,floor_number:int):
        self.id = uuid.uuid4()
        self.slot_type = slot_type
        self.floor_number = floor_number
        self.is_occupied = True
    
    def __str__(self):
        return f"ParkingSlot(id={self.id}, type={self.slot_type.value}, occupied={self.is_occupied}, floor={self.floor_number})"

