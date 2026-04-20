

from domain.message import Message
from domain.observer.subscriber_observer import SubscriberObserver


class EmailSubscriber(SubscriberObserver):
    def __init__(self, email: str):
        self.email = email

    def update(self, message: Message):
        print(f"Sending EMAIL to {self.email}: New message in topic -> {message.content}")