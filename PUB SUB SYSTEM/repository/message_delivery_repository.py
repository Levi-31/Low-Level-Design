




from abc import ABC, abstractmethod
from typing import List

from domain.delivery_status import DeliveryStatus
from domain.message_delivery import MessageDelivery


class MessageDeliveryRepository(ABC):
    @abstractmethod
    def save(self, delivery: MessageDelivery) -> MessageDelivery:
        pass

    @abstractmethod
    def find_pending_by_subscriber(self, subscriber_id: str) -> List[MessageDelivery]:
        pass

    @abstractmethod
    def update_delivery_status(self, delivery_id: str, status: DeliveryStatus):
        pass

    @abstractmethod
    def delete_by_id(self, delivery_id: str):
        pass