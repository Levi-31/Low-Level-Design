from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from domain.elevator import Elevator

class ElevatorStateHandler(ABC):
    @abstractmethod
    def handle_request(self, elevator: 'Elevator', request: Any) -> None:
        pass

    @abstractmethod
    def update_state(self, elevator: 'Elevator') -> None:
        pass

    @abstractmethod
    def get_state_name(self) -> str:
        pass