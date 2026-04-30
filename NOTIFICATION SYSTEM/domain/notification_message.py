

from typing import List

from domain.subscriber import Subscriber
from service.decorator.notification_decorator import BaseNotification


class NotificationMessage:
    def __init__(self, content: BaseNotification, users: List[Subscriber]):
        self.content = content
        self.users = users

    def get_message(self):
        return self.content.get_content()