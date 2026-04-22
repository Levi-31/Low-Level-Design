

from typing import List, Optional

from domain.elevator import Elevator
from domain.elevator_state import ElevatorState
from repository.elevator_repository import ElevatorRepository
from service.request_service import RequestService


class ElevatorService:
    def __init__(self, repository: ElevatorRepository) -> None:
        self.elevator_repository = repository
        self.request_service :Optional[RequestService] = None

    def set_request_service(self, service: RequestService) -> None:
        self.request_service = service

    def create_elevator(self, building_id: str, capacity: int) -> Elevator:
        elevator = Elevator(building_id, capacity)
        return self.elevator_repository.save(elevator)

    def update_elevator_state(self, elevator_id: str, state: ElevatorState) -> None:
        elevator = self.elevator_repository.find_by_id(elevator_id)
        if elevator:
            elevator.state = state
            self.elevator_repository.save(elevator)

    def update_elevator_floor(self, elevator_id: str, floor: int) -> None:
        elevator = self.elevator_repository.find_by_id(elevator_id)
        if elevator:
            elevator.current_floor = floor
            self.elevator_repository.save(elevator)

    def get_available_elevators(self, building_id: str) -> List[Elevator]:
        return self.elevator_repository.find_available_elevators(building_id)

    def get_elevators_by_building(self, building_id: str) -> List[Elevator]:
        return self.elevator_repository.find_by_building(building_id)

    def find_by_id(self, elevator_id: str) -> Optional[Elevator]:
        return self.elevator_repository.find_by_id(elevator_id)

    def set_maintenance_mode(self, elevator_id: str, maintenance: bool) -> None:
        elevator = self.elevator_repository.find_by_id(elevator_id)
        if elevator:
            if maintenance:
                if self.has_pending_requests(elevator_id) or self.has_assigned_requests(elevator_id):
                    elevator.state = ElevatorState.PRE_MAINTENANCE
                    print(f"Elevator {elevator_id} entering pre-maintenance mode to complete pending requests gracefully")
                else:
                    elevator.enter_maintenance()
            else:
                elevator.exit_maintenance()
            self.elevator_repository.save(elevator)

    def check_maintenance_transition(self, elevator_id: str) -> None:
        elevator = self.elevator_repository.find_by_id(elevator_id)
        if elevator and elevator.state == ElevatorState.PRE_MAINTENANCE:
            if not self.has_pending_requests(elevator_id):
                elevator.enter_maintenance()
                self.elevator_repository.save(elevator)
                print(f"Elevator {elevator_id} transitioned to maintenance mode")

    def has_pending_requests(self, elevator_id: str) -> bool:
        if not self.request_service: return False
        return len(self.request_service.get_pending_requests_for_elevator(elevator_id)) > 0

    def has_assigned_requests(self, elevator_id: str) -> bool:
        if not self.request_service: return False
        return len(self.request_service.get_assigned_requests_for_elevator(elevator_id)) > 0
