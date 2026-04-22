




from typing import List, Optional, Dict

from domain.internal_request import InternalRequest
from domain.request_status import RequestStatus


class InternalRequestRepository:
    def __init__(self):
        self._requests: Dict[str,InternalRequest]= {}

    def save(self, request: InternalRequest) -> InternalRequest:
        self._requests[request.id] = request
        return request

    def find_by_id(self, request_id: str) -> Optional[InternalRequest]:
        return self._requests.get(request_id)

    def find_by_elevator(self, elevator_id: str) -> List[InternalRequest]:
        return [r for r in self._requests.values() if r.elevator_id == elevator_id]

    def find_pending_by_elevator(self, elevator_id: str) -> List[InternalRequest]:
        return [r for r in self.find_by_elevator(elevator_id) if r.status == RequestStatus.PENDING]
