

from domain.notification_message import NotificationMessage


class NotificationService:
    def send(self, message: NotificationMessage) -> None:
        print(f"[Notification] to={message.to} subject={message.subject} body={message.body}")