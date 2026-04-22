


from typing import List, Optional

from domain.elevator import Elevator
from domain.external_request import ExternalRequest
from domain.strategy.elevator_selection_strategy import ElevatorSelectionStrategy


class NearestElevatorStrategy(ElevatorSelectionStrategy):
    def select_elevator(self, request: ExternalRequest, elevators: List[Elevator]) -> Optional[Elevator]:
        if not elevators:
            return None
        
        nearest_elevator = None
        min_distance = float('inf')
        
        for elevator in elevators:
            distance = abs(elevator.current_floor - request.floor_number)
            if distance < min_distance:
                min_distance = distance
                nearest_elevator = elevator
        
        return nearest_elevator

class LoadBalancingStrategy(ElevatorSelectionStrategy):
    # This would ideally need access to request loads, but we'll simplify
    def select_elevator(self, request: ExternalRequest, elevators: List[Elevator]) -> Optional[Elevator]:
        if not elevators:
            return None
        # Simply return the first available elevator as a placeholder for load balancing

        # We can use a min priority queue type structure to hold the minimum load elevator at the top
        return elevators[0]