

from enum import Enum


class TaskStatus(Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
