


from domain.subscription import Subscription
from service.subscription_service import SubscriptionService


class SubscriptionController:
    def __init__(self, subscription_service: SubscriptionService):
        self.subscription_service = subscription_service

    def subscribe_to_topic(self, topic_id: str, subscriber_id: str) -> Subscription:
        return self.subscription_service.subscribe_to_topic(topic_id, subscriber_id)

    def unsubscribe_from_topic(self, topic_id: str, subscriber_id: str):
        self.subscription_service.unsubscribe_from_topic(topic_id, subscriber_id)