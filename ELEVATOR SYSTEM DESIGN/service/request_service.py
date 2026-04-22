


from typing import List

from domain.direction import Direction
from domain.external_request import ExternalRequest
from domain.internal_request import InternalRequest
from domain.request_status import RequestStatus
from repository.external_request_repository import ExternalRequestRepository
from repository.internal_request_repository import InternalRequestRepository


class RequestService:
    def __init__(self, external_repo: ExternalRequestRepository, internal_repo: InternalRequestRepository) -> None:
        self.external_request_repository = external_repo
        self.internal_request_repository = internal_repo

    def create_external_request(self, floor: int, direction: Direction, building_id: str) -> ExternalRequest:
        request = ExternalRequest(building_id, floor, direction)
        return self.external_request_repository.save(request)

    def create_internal_request(self, elevator_id: str, destination_floor: int) -> InternalRequest:
        request = InternalRequest(elevator_id, destination_floor)
        return self.internal_request_repository.save(request)

    def complete_external_request(self, request_id: str) -> None:
        request = self.external_request_repository.find_by_id(request_id)
        if request:
            request.status = RequestStatus.COMPLETED
            self.external_request_repository.save(request)

    def complete_internal_request(self, request_id: str) -> None:
        request = self.internal_request_repository.find_by_id(request_id)
        if request:
            request.status = RequestStatus.COMPLETED
            self.internal_request_repository.save(request)

    def get_queued_requests(self, building_id: str) -> List[ExternalRequest]:
        all_reqs = self.external_request_repository.find_by_building(building_id)
        return [r for r in all_reqs if r.status == RequestStatus.QUEUED]

    def get_pending_requests_for_elevator(self, elevator_id: str) -> List[InternalRequest]:
        return self.internal_request_repository.find_pending_by_elevator(elevator_id)

    def assign_request_to_elevator(self, request_id: str, elevator_id: str) -> None:
        request = self.external_request_repository.find_by_id(request_id)
        if request:
            request.assigned_elevator_id = elevator_id
            request.status = RequestStatus.ASSIGNED
            self.external_request_repository.save(request)
            # Create internal request for movement
            self.create_internal_request(elevator_id, request.floor_number)
            print(f"Created internal request for elevator {elevator_id} to serve external request at floor {request.floor_number}")

    def get_assigned_requests_for_elevator(self, elevator_id: str) -> List[ExternalRequest]:
        all_reqs = self.external_request_repository.find_by_building("")
        return [r for r in all_reqs if r.assigned_elevator_id == elevator_id and r.status == RequestStatus.ASSIGNED]

    def get_pending_external_requests(self, building_id: str) -> List[ExternalRequest]:
        return self.external_request_repository.find_pending_by_building(building_id)
