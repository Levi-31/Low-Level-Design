


from dataclasses import dataclass, field
import time

from domain.subscription_tier import SubscriptionTier


@dataclass
class User:
    id: int
    username: str
    email: str
    name: str
    subscription_tier: SubscriptionTier
    created_at: int = field(default_factory=lambda: int(time.time()))