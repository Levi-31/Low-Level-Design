





from typing import Dict, List

from domain.delivery_status import DeliveryStatus
from domain.message_delivery import MessageDelivery
from repository.message_delivery_repository import MessageDeliveryRepository


class MessageDeliveryRepositoryImpl(MessageDeliveryRepository):
    def __init__(self):
        self._deliveries: Dict[str, MessageDelivery] = {}

    def save(self, delivery: MessageDelivery) -> MessageDelivery:
        self._deliveries[delivery.id] = delivery
        return delivery

    def find_pending_by_subscriber(self, subscriber_id: str) -> List[MessageDelivery]:
        return [d for d in self._deliveries.values() if d.subscriber_id == subscriber_id and d.status == DeliveryStatus.PENDING]

    def update_delivery_status(self, delivery_id: str, status: DeliveryStatus):
        if delivery_id in self._deliveries:
            self._deliveries[delivery_id].status = status

    def delete_by_id(self, delivery_id: str):
        if delivery_id in self._deliveries:
            del self._deliveries[delivery_id]