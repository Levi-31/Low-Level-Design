




import uuid

from domain.observer.real_time_subscriber import RealtimeSubscriber
from domain.subscriber import Subscriber
from repository.message_delivery_repository import MessageDeliveryRepository
from repository.subscriber_repository import SubscriberRepository
from repository.subscription_repository import SubscriptionRepository
from repository.topic_repository import TopicRepository


class SubscriberService:
    def __init__(self, subscriber_repository: SubscriberRepository,
                 subscription_repository: SubscriptionRepository,
                 message_delivery_repository: MessageDeliveryRepository,
                 topic_repository: TopicRepository):
        self.subscriber_repository = subscriber_repository
        self.subscription_repository = subscription_repository
        self.message_delivery_repository = message_delivery_repository
        self.topic_repository = topic_repository
    

    def register_subscriber(self, email: str) -> Subscriber:
        subscriber = Subscriber(str(uuid.uuid4()), email)
        return self.subscriber_repository.save(subscriber)

    def go_online(self, subscriber_id: str, connection_id: str):
        self.subscriber_repository.update_online_status(subscriber_id, True, connection_id)


        subscriber = self.subscriber_repository.find_by_id(subscriber_id)

        if subscriber:
            # Re-add to all subscribed topics' realtime lists
            subscriptions = self.subscription_repository.find_by_subscriber(subscriber_id)
            for sub in subscriptions:
                if sub.active:
                    topic = self.topic_repository.find_by_id(sub.topic_id)
                    if topic:
                        topic.message_subject.add_realtime_subscriber(
                            RealtimeSubscriber(connection_id, subscriber_id))
            
            self.push_pending_deliveries(subscriber_id)


    def go_offline(self, subscriber_id: str):
        self.subscriber_repository.update_online_status(subscriber_id, False, None)


    def push_pending_deliveries(self, subscriber_id: str):
        print(f"Pushing pending deliveries for subscriber: {subscriber_id}")