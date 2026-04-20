


from abc import ABC, abstractmethod
from typing import List, Optional

from domain.subscriber import Subscriber


class SubscriberRepository(ABC):
    @abstractmethod
    def save(self, subscriber: Subscriber) -> Subscriber:
        pass

    @abstractmethod
    def find_by_id(self, subscriber_id: str) -> Optional[Subscriber]:
        pass

    @abstractmethod
    def find_all(self) -> List[Subscriber]:
        pass

    @abstractmethod
    def update_online_status(self, subscriber_id: str, is_online: bool, connection_id: str):
        pass

    @abstractmethod
    def delete_by_id(self, subscriber_id: str):
        pass