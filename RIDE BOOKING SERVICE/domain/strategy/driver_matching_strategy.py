
from abc import ABC, abstractmethod
from typing import List

from domain.driver import Driver
from domain.location import Location

class DriverMatchingStrategy(ABC):
    @abstractmethod
    def find_matching_drivers(self, pickup: Location,candidates: List[Driver], max_results: int) -> List[Driver]:
        pass