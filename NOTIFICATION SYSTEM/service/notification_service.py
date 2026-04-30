

from typing import List

from domain.notification_message import NotificationMessage
from domain.subscriber import Subscriber
from repository.notification_repository import NotificationRepository
from service.decorator.notification_decorator import SignatureDecorator, SimpleNotification, TimeStampDecorator
from service.observer.notification_observer import NotificationObservable



class NotificationService:
    def __init__(self, repo: NotificationRepository, observable: NotificationObservable):
        self.repo = repo
        self.observable = observable

    def process_notification(self, text: str, users: List[Subscriber]):
        content = SimpleNotification(text)
        content = TimeStampDecorator(content)
        content = SignatureDecorator(content)

        notification = NotificationMessage(content, users)

        self.repo.save(notification)
        self.observable.notify(notification)
