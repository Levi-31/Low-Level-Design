

from service.notification.notification_channel import NotificationChannel
from service.notification.notification_message import NotificationMessage


class EmailNotificationChannel(NotificationChannel):
    # TODO: Integrate with email provider (SMTP/API)
    def send(self, message: NotificationMessage):
        print(f"[EMAIL] To: {message.to} | Subject: {message.subject} | Body: {message.body}")