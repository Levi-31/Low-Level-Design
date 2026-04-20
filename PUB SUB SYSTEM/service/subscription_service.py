




import uuid

from domain.observer.email_subscriber import EmailSubscriber
from domain.observer.real_time_subscriber import RealtimeSubscriber
from domain.subscription import Subscription
from repository.subscriber_repository import SubscriberRepository
from repository.subscription_repository import SubscriptionRepository
from repository.topic_repository import TopicRepository


class SubscriptionService:
    def __init__(self, subscription_repository: SubscriptionRepository, 
                 subscriber_repository: SubscriberRepository, 
                 topic_repository: TopicRepository):
        self.subscription_repository = subscription_repository
        self.subscriber_repository = subscriber_repository
        self.topic_repository = topic_repository

    def subscribe_to_topic(self, topic_id: str, subscriber_id: str) -> Subscription:
        topic = self.topic_repository.find_by_id(topic_id)
        subscriber = self.subscriber_repository.find_by_id(subscriber_id)

        if not topic: raise Exception("Topic not found")
        if not subscriber: raise Exception("Subscriber not found")

        subscription = Subscription(str(uuid.uuid4()), topic_id, subscriber_id)
        self.subscription_repository.save(subscription)

        # Add Email observer
        topic.message_subject.add_email_subscriber(EmailSubscriber(subscriber.email))

        # If online, add Realtime observer
        if subscriber.is_online:
            topic.message_subject.add_realtime_subscriber(
                RealtimeSubscriber(subscriber.realtime_connection_id, subscriber.id))

        return subscription

    def unsubscribe_from_topic(self, topic_id: str, subscriber_id: str):
        self.subscription_repository.deactivate_subscription(topic_id, subscriber_id)
