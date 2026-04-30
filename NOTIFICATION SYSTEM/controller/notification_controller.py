



from typing import List

from domain.subscriber import Subscriber
from service.notification_service import NotificationService


class NotificationController:
    def __init__(self, service: NotificationService):
        self.service = service

    def send_notification(self, text: str,users:List[Subscriber]):
        self.service.process_notification(text,users)