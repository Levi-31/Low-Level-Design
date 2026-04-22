




from domain.system_state import SystemState
from repository.building_repository import BuildingRepository
from repository.elevator_repository import ElevatorRepository
from repository.external_request_repository import ExternalRequestRepository
from repository.internal_request_repository import InternalRequestRepository
from service.building_service import BuildingService
from service.dispatcher_service import DispatcherService
from service.elevator_service import ElevatorService
from service.movement_service import MovementService
from service.request_service import RequestService


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from domain.elevator import Elevator

class ElevatorController:
    def __init__(self) -> None:
        self.elevator_repo = ElevatorRepository()
        self.building_repo = BuildingRepository()
        self.external_req_repo = ExternalRequestRepository()
        self.internal_req_repo = InternalRequestRepository()

        self.elevator_service = ElevatorService(self.elevator_repo)
        self.building_service = BuildingService(self.building_repo)
        self.request_service = RequestService(self.external_req_repo, self.internal_req_repo)

        self.dispatcher_service = DispatcherService(self.request_service, self.elevator_service)
        self.movement_service = MovementService(
            self.elevator_service, self.request_service, 
            self.building_service, self.dispatcher_service
        )

        self.elevator_service.set_request_service(self.request_service)

    

    def create_elevator(self, building_id: str, capacity: int) -> 'Elevator':
        if not self.building_service.building_exists(building_id):
            raise ValueError(f"Building not found: {building_id}")
        return self.elevator_service.create_elevator(building_id, capacity)
    

    def move_elevator(self, elevator_id: str, target_floor: int) -> None:
        elevator = self.elevator_service.find_by_id(elevator_id)
        if not elevator:
            raise ValueError("Elevator not found")
        if not self.building_service.is_valid_floor(elevator.building_id, target_floor):
            raise ValueError("Invalid floor number")
        
        self.request_service.create_internal_request(elevator_id, target_floor)
        print(f"Move request created for elevator {elevator_id} to floor {target_floor}")

    def set_elevator_maintenance(self, elevator_id: str, maintenance: bool) -> None:
        self.elevator_service.set_maintenance_mode(elevator_id, maintenance)
        print(f"Elevator {elevator_id} maintenance mode: {'ON' if maintenance else 'OFF'}")

    def start_elevator_system(self, building_id: str) -> None:
        if not self.building_service.is_system_running(building_id):
            self.building_service.set_building_system_state(building_id, SystemState.RUNNING)
            print(f"Elevator system started for building: {building_id}")
        else:
            print("Elevator system is already running")

    def stop_elevator_system(self, building_id: str) -> None:
        if self.building_service.is_system_running(building_id):
            self.building_service.set_building_system_state(building_id, SystemState.STOPPED)
            print(f"Elevator system stopped for building: {building_id}")
        else:
            print("Elevator system is not running")