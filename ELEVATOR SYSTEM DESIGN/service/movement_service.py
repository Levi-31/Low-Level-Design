


from domain.direction import Direction
from domain.elevator import Elevator
from domain.elevator_state import ElevatorState
from domain.strategy.movement_strategy_implementation import ScanStrategy
from service.elevator_service import ElevatorService


from domain.strategy.movement_strategy import MovementStrategy

class MovementService:
    def __init__(self, elev_service: ElevatorService, req_service: 'RequestService', bld_service: 'BuildingService', disp_service: 'DispatcherService') -> None:
        self.elevator_service: ElevatorService = elev_service
        self.request_service = req_service
        self.building_service = bld_service
        self.dispatcher_service = disp_service
        self.movement_strategy = ScanStrategy()

    def set_movement_strategy(self, strategy: MovementStrategy) -> None:
        self.movement_strategy = strategy

    def process_all_elevator_movements(self, building_id: str) -> None:
        elevators = self.elevator_service.get_elevators_by_building(building_id)
        for elevator in elevators:
            if elevator.is_active():
                self.process_elevator_movement(elevator.id, elevator)

    def process_elevator_movement(self, elevator_id: str, elevator: Elevator) -> None:
        pending_requests = self.request_service.get_pending_requests_for_elevator(elevator_id)

        if not pending_requests:
            if elevator.is_preparing_for_maintenance():
                self.elevator_service.check_maintenance_transition(elevator_id)
                return

            if elevator.direction != Direction.IDLE:
                elevator.direction = Direction.IDLE
                elevator.state = ElevatorState.STOPPED
                self.elevator_service.update_elevator_state(elevator_id, ElevatorState.STOPPED)
            return

        path = self.movement_strategy.calculate_path(elevator, pending_requests)

        if path:
            next_floor = path[0]
            current_floor = elevator.current_floor

            if next_floor > current_floor:
                elevator.direction = Direction.UP
                elevator.state = ElevatorState.MOVING
                elevator.current_floor += 1
                print(f"Elevator {elevator_id} moving UP to floor {elevator.current_floor}")
            elif next_floor < current_floor:
                elevator.direction = Direction.DOWN
                elevator.state = ElevatorState.MOVING
                elevator.current_floor -= 1
                print(f"Elevator {elevator_id} moving DOWN to floor {elevator.current_floor}")
            else:
                # Reached destination
                elevator.direction = Direction.IDLE
                elevator.state = ElevatorState.STOPPED
                elevator.open_doors()
                
                # Mark internal requests for this floor as completed
                for req in pending_requests:
                    if req.destination_floor == current_floor:
                        self.request_service.complete_internal_request(req.id)
                
                # Mark external requests assigned to this elevator at this floor as completed
                assigned_ext = self.request_service.get_assigned_requests_for_elevator(elevator_id)
                for req in assigned_ext:
                    if req.floor_number == current_floor:
                        self.request_service.complete_external_request(req.id)

                elevator.close_doors()
            
            self.elevator_service.update_elevator_state(elevator_id, elevator.state)

    def has_pending_requests(self, building_id: str) -> bool:
        elevators = self.elevator_service.get_elevators_by_building(building_id)
        for e in elevators:
            if self.request_service.get_pending_requests_for_elevator(e.id):
                return True
        return self.dispatcher_service.get_queue_size() > 0
