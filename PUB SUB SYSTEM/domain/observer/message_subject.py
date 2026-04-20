


from threading import Lock
from typing import List

from domain.message import Message
from domain.observer.subscriber_observer import SubscriberObserver


class MessageSubject:
    def __init__(self):
        self._email_subscribers: List[SubscriberObserver] = []
        self._realtime_subscribers: List[SubscriberObserver] = []
        self._lock = Lock()
    

    def add_email_subscriber(self,subscriber:SubscriberObserver):
        with self._lock:
            self._email_subscribers.append(subscriber)

    def remove_email_subscriber(self, subscriber: SubscriberObserver):
        with self._lock:
            if subscriber in self._email_subscribers:
                self._email_subscribers.remove(subscriber)
    
    def add_realtime_subscriber(self, subscriber: SubscriberObserver):
        with self._lock:
            self._realtime_subscribers.append(subscriber)


    def remove_realtime_subscriber(self, subscriber: SubscriberObserver):
        with self._lock:
            if subscriber in self._realtime_subscribers:
                self._realtime_subscribers.remove(subscriber)


    def notify(self, message: Message):
        self.notify_email_subscribers(message)
        self.notify_realtime_subscribers(message)


    def notify_email_subscribers(self, message: Message):
        with self._lock:
            subscribers = list(self._email_subscribers)
        for sub in subscribers:
            sub.update(message)

    def notify_realtime_subscribers(self, message: Message):
        with self._lock:
            subscribers = list(self._realtime_subscribers)
        for sub in subscribers:
            sub.update(message)


    @property
    def email_subscribers(self):
        with self._lock:
            return list(self._email_subscribers)

    @property
    def realtime_subscribers(self):
        with self._lock:
            return list(self._realtime_subscribers)