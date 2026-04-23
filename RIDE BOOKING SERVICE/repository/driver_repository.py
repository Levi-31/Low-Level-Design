from abc import ABC, abstractmethod
from typing import List, Optional

from domain.driver import Driver
from domain.driver_status import DriverStatus


class DriverRepository(ABC):
    @abstractmethod
    def find_by_id(self, driver_id: str) -> Optional[Driver]:
        pass

    @abstractmethod
    def save(self, driver: Driver) -> None:
        pass

    @abstractmethod
    def find_by_status(self, status: DriverStatus) -> List[Driver]:
        pass