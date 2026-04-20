
from typing import Dict, List
from domain.subscription import Subscription
from repository.subscription_repository import SubscriptionRepository


class SubscriptionRepositoryImpl(SubscriptionRepository):
    def __init__(self):
        self._subscriptions: Dict[str, Subscription] = {}

    def save(self, subscription: Subscription) -> Subscription:
        self._subscriptions[subscription.id] = subscription
        return subscription

    def find_by_topic(self, topic_id: str) -> List[Subscription]:
        return [s for s in self._subscriptions.values() if s.topic_id == topic_id]

    def find_by_subscriber(self, subscriber_id: str) -> List[Subscription]:
        return [s for s in self._subscriptions.values() if s.subscriber_id == subscriber_id]

    def deactivate_subscription(self, topic_id: str, subscriber_id: str):
        for s in self._subscriptions.values():
            if s.topic_id == topic_id and s.subscriber_id == subscriber_id:
                s.active = False

    def delete_by_id(self, subscription_id: str):
        if subscription_id in self._subscriptions:
            del self._subscriptions[subscription_id]