


from domain.notification_message import NotificationMessage


class NotificationRepository:
    def __init__(self):
        self.storage = []

    def save(self, notification: NotificationMessage):
        self.storage.append(notification)

    def get_all(self):
        return self.storage