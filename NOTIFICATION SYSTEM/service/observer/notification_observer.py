



from abc import ABC, abstractmethod
from typing import Dict, List

from domain.notification_channel import NotificationChannel
from domain.notification_message import NotificationMessage
from service.strategy.notification_strategy import NotificationStrategy




class NotificationObserver(ABC):
    
    @abstractmethod
    def update(self, notification: NotificationMessage):
        pass



class NotificationObservable:
    def __init__(self):
        self.observers: List[NotificationObserver] = []

    def add(self, observer: NotificationObserver):
        self.observers.append(observer)

    def notify(self, notification):
        for obs in self.observers:
            obs.update(notification)




class Logger(NotificationObserver):
    def update(self, notification:NotificationMessage):
        print(f"[LOG] {notification.get_message()}")


class NotificationEngine(NotificationObserver):
    def __init__(self, strategies: List[NotificationStrategy]):
        self.strategy_map: Dict[NotificationChannel, NotificationStrategy] = {
            strategy.channel(): strategy for strategy in strategies
        }

    def update(self, notification: NotificationMessage):
        message = notification.get_message()

        for user in notification.users:
            for channel in user.channels:
                strategy = self.strategy_map.get(channel)

                if strategy:
                    try:
                        strategy.send(user, message)
                    except Exception as e:
                        print(f"[ERROR] Failed to send {channel.value} to {user.user_id}: {e}")


