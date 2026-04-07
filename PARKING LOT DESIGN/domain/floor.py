
import uuid

from domain.parking_slot import ParkingSlot
from domain.Vehicle import Vehicle


class Floor:
    def __init__(self,floor_number:int):
        self.id = uuid.uuid4()
        self.floor_number = floor_number
        self.slots : list[ParkingSlot] = []
    

    def add_slots(self,slot:ParkingSlot):
        self.slots.append(slot)
    
    def get_available_parking_slot(self,vehicle_type:Vehicle.VehicleType) -> list[ParkingSlot]:
        return [slot for slot in self.slots if slot.slot_type == vehicle_type and not slot.is_occupied]

    def get_available_slot_count(self,vehicle_type:Vehicle.VehicleType) -> int:
        return len(self.get_available_parking_slot(vehicle_type))
