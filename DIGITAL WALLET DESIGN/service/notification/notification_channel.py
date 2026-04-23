


from abc import ABC, abstractmethod

from service.notification.notification_message import NotificationMessage


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message: NotificationMessage):
        pass
    