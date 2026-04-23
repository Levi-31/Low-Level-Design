

from service.notification.notification_channel import NotificationChannel
from service.notification.notification_message import NotificationMessage


class SmsNotificationChannel(NotificationChannel):
    # TODO: Integrate with SMS provider (e.g., Twilio)
    def send(self, message: NotificationMessage):
        print(f"[SMS] To: {message.to} | Body: {message.body}")