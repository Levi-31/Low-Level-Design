


from typing import List

from domain.notification_channel import NotificationChannel


class Subscriber:
    def __init__(self, user_id: str, channels: List[NotificationChannel]):
        self.user_id = user_id
        self.channels = channels
    
    