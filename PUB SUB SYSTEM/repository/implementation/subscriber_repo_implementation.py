
from typing import Dict, List, Optional

from domain.subscriber import Subscriber
from repository.subscriber_repository import SubscriberRepository


class SubscriberRepositoryImpl(SubscriberRepository):
    def __init__(self):
        self._subscribers: Dict[str, Subscriber] = {}

    def save(self, subscriber: Subscriber) -> Subscriber:
        self._subscribers[subscriber.id] = subscriber
        return subscriber

    def find_by_id(self, subscriber_id: str) -> Optional[Subscriber]:
        return self._subscribers.get(subscriber_id)

    def find_all(self) -> List[Subscriber]:
        return list(self._subscribers.values())

    def update_online_status(self, subscriber_id: str, is_online: bool, connection_id: str):
        if subscriber_id in self._subscribers:
            sub = self._subscribers[subscriber_id]
            sub.is_online = is_online
            sub.realtime_connection_id = connection_id

    def delete_by_id(self, subscriber_id: str):
        if subscriber_id in self._subscribers:
            del self._subscribers[subscriber_id]