

from domain.delivery_channels import DeliveryChannel
from domain.delivery_status import DeliveryStatus


class MessageDelivery:
    def __init__(self, id: str, message_id: str, subscriber_id: str, channel: DeliveryChannel):
        self.id = id
        self.message_id = message_id
        self.subscriber_id = subscriber_id
        self.channel = channel
        self.status = DeliveryStatus.PENDING
        self.created_at = 0
        self.acknowledged_at = 0