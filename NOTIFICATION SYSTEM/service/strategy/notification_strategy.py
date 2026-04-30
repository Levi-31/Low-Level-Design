

from abc import ABC , abstractmethod

from domain.notification_channel import NotificationChannel
from domain.subscriber import Subscriber


class NotificationStrategy(ABC):
    @abstractmethod
    def channel(self) -> NotificationChannel:
        pass

    @abstractmethod
    def send(self, user: Subscriber, content: str):
        pass


class EmailStrategy(NotificationStrategy):
    def channel(self) -> NotificationChannel:
        return  NotificationChannel.EMAIL

    def send(self, user: Subscriber, content: str):
        print(f"[EMAIL to {user.user_id}] {content}")


class SMSStrategy(NotificationStrategy):
    def channel(self) -> NotificationChannel:
        return  NotificationChannel.SMS

    def send(self, user: Subscriber, content: str):
        print(f"[SMS to {user.user_id}] {content}")


class PushStrategy(NotificationStrategy):
    def channel(self) -> NotificationChannel:
        return  NotificationChannel.PUSH

    def send(self, user: Subscriber, content: str):
        print(f"[PUSH to {user.user_id}] {content}")