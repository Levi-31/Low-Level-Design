


from abc import ABC , abstractmethod
from typing import List

from domain.elevator import Elevator
from domain.internal_request import InternalRequest


class MovementStrategy(ABC):
    @abstractmethod
    def calculate_path(self, elevator: Elevator, requests: List[InternalRequest]) -> List[int]:
        pass