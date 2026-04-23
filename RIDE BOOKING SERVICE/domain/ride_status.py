


from enum import Enum, auto


class RideStatus(Enum):
    REQUESTED = auto()
    ASSIGNED = auto()
    ACCEPTED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    DENIED = auto()