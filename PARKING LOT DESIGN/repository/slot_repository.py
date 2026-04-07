from typing import Dict, List, Optional

from domain.Vehicle import Vehicle
from domain.parking_slot import ParkingSlot


class SlotRepository:
    def __init__(self):
        self._slots :dict[str,ParkingSlot] = {}
    

    def save(self,slot:ParkingSlot) -> ParkingSlot:
        self._slots[slot.id] = slot
        return slot
    
    def find_by_id(self,slot_id:str) -> Optional[ParkingSlot]:
        return self._slots.get(slot_id)

    def find_available_slots(self, vehicle_type: Vehicle.VehicleType) -> List[ParkingSlot]:
        return [slot for slot in self._slots.values() if slot.slot_type == vehicle_type and not slot.is_occupied]
    
    def allocate_slot(self,vehicle_type:Vehicle.VehicleType) -> Optional[ParkingSlot]:
        for slot in self._slots.values():
            if slot.slot_type == vehicle_type and not slot.is_occupied :
                self.is_occupied = True
                return slot
        
        return None
    
    def release_slot(self,slot_id:str):
        slot = self._slots.get(slot_id)
        if slot:
            slot.is_occupied = False


    def get_slot_statistics(self) -> Dict[str, int]:
        stats = {}
        for slot in self._slots.values():
            stats[slot.slot_type.value] = stats.get(slot.slot_type.value, 0) + 1
        return stats



    

