



from domain.request_status import RequestStatus
from service.dispatcher_service import DispatcherService
from service.elevator_service import ElevatorService
from service.movement_service import MovementService
from service.request_service import RequestService


class ElevatorSchedulerService:
    def __init__(self, elev_service: ElevatorService, req_service: RequestService, mov_service: MovementService, disp_service: DispatcherService) -> None:
        self.elevator_service: ElevatorService = elev_service
        self.request_service :RequestService = req_service
        self.movement_service :MovementService = mov_service
        self.dispatcher_service : DispatcherService = disp_service
        self.building_schedulers = {}

    def start_building_scheduler(self, building_id: str) -> None:
        self.building_schedulers[building_id] = True
        print(f"Elevator scheduler started for building: {building_id}")

    def stop_building_scheduler(self, building_id: str) -> None:
        self.building_schedulers[building_id] = False
        print(f"Elevator scheduler stopped for building: {building_id}")

    def is_scheduler_running(self, building_id: str) -> bool:
        return self.building_schedulers.get(building_id, False)

    def process_building_operations(self, building_id: str) -> None:
        if not self.is_scheduler_running(building_id):
            return

        try:
            self._process_external_requests(building_id)
            self._process_elevator_movements(building_id)
        except Exception as e:
            print(f"Error processing building operations for {building_id}: {e}")

    def _process_external_requests(self, building_id: str) -> None:
        pending_requests = self.request_service.get_pending_external_requests(building_id)
        for request in pending_requests:
            if request.status in [RequestStatus.PENDING, RequestStatus.QUEUED]:
                print(f"Scheduler: Processing external request: {request.id}")
                self.dispatcher_service.process_external_request(request, building_id)

    def _process_elevator_movements(self, building_id: str) -> None:
        elevators = self.elevator_service.get_elevators_by_building(building_id)
        for elevator in elevators:
            if not elevator.is_active():
                continue

            pending_internal = self.request_service.get_pending_requests_for_elevator(elevator.id)
            if pending_internal:
                print(f"Scheduler: Processing movement for elevator: {elevator.id}")
                self.movement_service.process_elevator_movement(elevator.id, elevator)

            if elevator.is_preparing_for_maintenance():
                self.elevator_service.check_maintenance_transition(elevator.id)
