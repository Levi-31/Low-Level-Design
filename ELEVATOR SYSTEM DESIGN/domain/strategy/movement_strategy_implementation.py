




from typing import List

from domain.elevator import Elevator
from domain.internal_request import InternalRequest
from domain.strategy.movement_strategy import MovementStrategy


class FCFSStrategy(MovementStrategy):
    #FIRST COME FIRST SERVED STRATEGY
    def calculate_path(self, elevator: Elevator, requests: List[InternalRequest]) -> List[int]:
        if not requests:
            return []
        return [requests[0].destination_floor]

class ScanStrategy(MovementStrategy):
    def calculate_path(self, elevator: Elevator, requests: List[InternalRequest]) -> List[int]:
        if not requests:
            return []
        
        floors = sorted(list(set(r.destination_floor for r in requests)))
        # Simplified SCAN: just go to the closest one in the current direction 
        # or the overall closest if idle.
        current_floor = elevator.current_floor
        
        # Logic to pick next floor based on direction...
        # For simplicity in this LLD, we'll just pick the nearest floor
        return [min(floors, key=lambda f: abs(f - current_floor))]
