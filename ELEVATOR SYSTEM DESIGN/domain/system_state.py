from enum import Enum

class SystemState(Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    MAINTENANCE = "MAINTENANCE"