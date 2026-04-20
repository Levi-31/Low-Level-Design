





from domain.message import Message
from service.publisher_service import PublisherService


class PublisherController:
    def __init__(self, publisher_service: PublisherService):
        self.publisher_service = publisher_service

    def publish_message(self, topic_id: str, content: str) -> Message:
        return self.publisher_service.publish_message(topic_id, content)