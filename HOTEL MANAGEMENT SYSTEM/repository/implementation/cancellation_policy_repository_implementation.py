from typing import Optional, Dict
from domain.cancellation_policy import CancellationPolicy
from repository.cancellation_policy_repository import CancellationPolicyRepository


class CancellationPolicyRepositoryImpl(CancellationPolicyRepository):
    def __init__(self):
        self.policies: Dict[str, CancellationPolicy] = {}

    def save(self, policy: CancellationPolicy) -> CancellationPolicy:
        self.policies[policy.id] = policy
        return policy

    def find_by_id(self, policy_id: str) -> Optional[CancellationPolicy]:
        return self.policies.get(policy_id)


