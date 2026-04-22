

from typing import Dict, List, Optional
from domain.elevator import Elevator

class ElevatorRepository:
    def __init__(self):
        self._elevators : Dict[str, Elevator] = {}

    def save(self, elevator: Elevator) -> Elevator:
        self._elevators[elevator.id] = elevator
        return elevator

    def find_by_id(self, elevator_id: str) -> Optional[Elevator]:
        return self._elevators.get(elevator_id)

    def find_by_building(self, building_id: str) -> List[Elevator]:
        return [e for e in self._elevators.values() if e.building_id == building_id]

    def find_available_elevators(self, building_id: str) -> List[Elevator]:
        return [e for e in self.find_by_building(building_id) if e.can_accept_external_requests()]
