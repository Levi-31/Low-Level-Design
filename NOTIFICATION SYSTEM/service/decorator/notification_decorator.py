

from abc import ABC , abstractmethod
from datetime import datetime


class BaseNotification(ABC):
    @abstractmethod
    def get_content(self) -> str:
        pass


class SimpleNotification(BaseNotification):
    def __init__(self,text:str):
        self.text = text

    def get_content(self):
        return self.text


class NotificationDecorator(BaseNotification):
    def __init__(self,notification:BaseNotification):
        self.notification = notification

    def get_content(self):
        return self.notification.get_content()


class TimeStampDecorator(NotificationDecorator):
    def get_content(self) -> str:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{current_time}] {super().get_content()}"


class SignatureDecorator(NotificationDecorator):
    def get_content(self) -> str:
        return f"{super().get_content()} -- Team"
