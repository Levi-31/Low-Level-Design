



from typing import Dict, List, Optional

from domain.external_request import ExternalRequest
from domain.request_status import RequestStatus


class ExternalRequestRepository:
    def __init__(self):
        self._requests:Dict[str,ExternalRequest] = {}

    def save(self, request: ExternalRequest) -> ExternalRequest:
        self._requests[request.id] = request
        return request

    def find_by_id(self, request_id: str) -> Optional[ExternalRequest]:
        return self._requests.get(request_id)

    def find_by_building(self, building_id: str) -> List[ExternalRequest]:
        if not building_id:
            return list(self._requests.values())
        return [r for r in self._requests.values() if r.building_id == building_id]

    def find_pending_by_building(self, building_id: str) -> List[ExternalRequest]:
        return [r for r in self.find_by_building(building_id) if r.status in [RequestStatus.PENDING, RequestStatus.QUEUED]]
