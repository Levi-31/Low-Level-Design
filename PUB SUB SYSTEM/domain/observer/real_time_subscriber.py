

from domain.message import Message
from domain.observer.subscriber_observer import SubscriberObserver


class RealtimeSubscriber(SubscriberObserver):
    def __init__(self, connection_id: str, subscriber_id: str):
        self.connection_id = connection_id
        self.subscriber_id = subscriber_id

    def update(self, message: Message):
        print(f"Sending REALTIME to {self.subscriber_id} (connection: {self.connection_id}): New message -> {message.content}")