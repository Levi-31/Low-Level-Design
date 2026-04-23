from abc import ABC, abstractmethod
from typing import Optional
from domain.rider import Rider


class RiderRepository(ABC):
    @abstractmethod
    def find_by_id(self, rider_id: str) -> Optional[Rider]:
        pass

    @abstractmethod
    def save(self, rider: Rider) -> None:
        pass