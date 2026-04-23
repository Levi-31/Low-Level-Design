

from typing import Dict

from service.notification.notification_channel import NotificationChannel
from service.notification.notification_message import NotificationMessage


class NotificationRouter:
    def __init__(self):
        self._channels: Dict[str, NotificationChannel] = {}

    def register_channel(self, channel_name: str, channel: NotificationChannel):
        self._channels[channel_name] = channel

    def send(self, channel_name: str, message: NotificationMessage):
        """Send to a specific channel by name (e.g., 'email', 'sms')."""
        channel = self._channels.get(channel_name)
        if channel:
            channel.send(message)

    def send_all(self, message: NotificationMessage):
        """Broadcast to all registered channels."""
        for channel in self._channels.values():
            channel.send(message)