


from enum import Enum

class RequestStatus(Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    COMPLETED = "COMPLETED"
    QUEUED = "QUEUED"