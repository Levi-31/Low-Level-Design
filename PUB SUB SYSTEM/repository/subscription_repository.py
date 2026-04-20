




from abc import ABC, abstractmethod
from typing import List

from domain.subscription import Subscription


class SubscriptionRepository(ABC):
    @abstractmethod
    def save(self, subscription: Subscription) -> Subscription:
        pass

    @abstractmethod
    def find_by_topic(self, topic_id: str) -> List[Subscription]:
        pass

    @abstractmethod
    def find_by_subscriber(self, subscriber_id: str) -> List[Subscription]:
        pass

    @abstractmethod
    def deactivate_subscription(self, topic_id: str, subscriber_id: str):
        pass

    @abstractmethod
    def delete_by_id(self, subscription_id: str):
        pass