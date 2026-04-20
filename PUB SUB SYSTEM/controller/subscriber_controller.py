


from domain.subscriber import Subscriber
from service.subscriber_service import SubscriberService


class SubscriberController:
    def __init__(self, subscriber_service: SubscriberService):
        self.subscriber_service = subscriber_service

    def register_subscriber(self, email: str) -> Subscriber:
        return self.subscriber_service.register_subscriber(email)

    def go_online(self, subscriber_id: str, connection_id: str):
        self.subscriber_service.go_online(subscriber_id, connection_id)

    def go_offline(self, subscriber_id: str):
        self.subscriber_service.go_offline(subscriber_id)