



from queue import Queue
import threading

from domain.external_request import ExternalRequest
from domain.strategy.elevator_selection_strategy_implementation import NearestElevatorStrategy
from service.elevator_service import ElevatorService


from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from service.request_service import RequestService

class DispatcherService:
    def __init__(self, req_service: 'RequestService', elev_service: ElevatorService) -> None:
        self.request_service = req_service
        self.elevator_service = elev_service
        self.selection_strategy = NearestElevatorStrategy()
        self.request_queue = Queue()
        self.queue_lock = threading.Lock()

    def queue_external_request(self, request: ExternalRequest) -> None:
        with self.queue_lock:
            self.request_queue.put(request)
            print(f"Request queued: Floor {request.floor_number} {request.direction.value}")


    def select_best_elevator(self, request: ExternalRequest, available_elevators: list) -> Optional[object]:
        return self.selection_strategy.select_elevator(request, available_elevators)
    
    def assign_request_to_elevator(self, request: ExternalRequest, elevator: object) -> None:
        self.request_service.assign_request_to_elevator(request.id, elevator.id)
        print(f"Request assigned: Floor {request.floor_number} -> Elevator {elevator.id}")

    def process_external_request(self, request: ExternalRequest, building_id: str) -> None:
        available_elevators = self.elevator_service.get_available_elevators(building_id)
        selected_elevator = self.select_best_elevator(request, available_elevators)
        if selected_elevator:
            self.assign_request_to_elevator(request, selected_elevator)
        else:
            self.queue_external_request(request)

    def get_queue_size(self) -> int:
        return self.request_queue.qsize()
    

    def process_pending_requests(self, building_id: str) -> None:
        with self.queue_lock:
            size = self.get_queue_size()
            for _ in range(size):
                request = self.request_queue.get()
                if request.building_id != building_id:
                    self.request_queue.put(request)
                    continue
                
                available_elevators = self.elevator_service.get_available_elevators(building_id)
                selected_elevator = self.select_best_elevator(request, available_elevators)
                if selected_elevator:
                    self.assign_request_to_elevator(request, selected_elevator)
                else:
                    self.request_queue.put(request)
