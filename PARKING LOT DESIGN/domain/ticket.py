from datetime import datetime
import uuid


class Ticket:
    def __init__(self,vehicle_id:str , slot_id:str):
        self.id = uuid.uuid4()
        self.vehicle_id = vehicle_id
        self.slot_id =  slot_id
        self.entry_time = (datetime.now())
        self.is_active = True

    
    def deactivate(self):
        self.is_active = False

    def __str__(self):
        return f"Ticket(id={self.id}, vehicle={self.vehicle_id}, slot={self.slot_id}, active={self.is_active})"