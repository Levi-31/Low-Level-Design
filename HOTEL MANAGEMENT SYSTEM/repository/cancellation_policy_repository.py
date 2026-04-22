

from abc import ABC, abstractmethod
from typing import Optional
from domain.cancellation_policy import CancellationPolicy

class CancellationPolicyRepository(ABC):
    @abstractmethod
    def save(self, policy: CancellationPolicy) -> CancellationPolicy:
        pass

    @abstractmethod
    def find_by_id(self, policy_id: str) -> Optional[CancellationPolicy]:
        pass
