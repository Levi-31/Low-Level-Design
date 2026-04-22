
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.elevator import Elevator
from domain.external_request import ExternalRequest


class ElevatorSelectionStrategy(ABC):
    @abstractmethod
    def select_elevator(self, request: ExternalRequest, elevators: List[Elevator]) -> Optional[Elevator]:
        pass