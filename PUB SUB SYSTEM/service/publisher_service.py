




import threading
import time
import uuid

from domain.message import Message
from domain.topic import Topic
from repository.message_delivery_repository import MessageDeliveryRepository
from repository.message_repository import MessageRepository
from repository.topic_repository import TopicRepository


class PublisherService:
    def __init__(self, topic_repository: TopicRepository,
                 message_repository: MessageRepository,
                 message_delivery_repository: MessageDeliveryRepository):
        self.topic_repository = topic_repository
        self.message_repository = message_repository
        self.message_delivery_repository = message_delivery_repository

    def publish_message(self, topic_id: str, content: str) -> Message:
        topic = self.topic_repository.find_by_id(topic_id)
        if not topic:
            raise Exception(f"Topic not found: {topic_id}")
        
        if not topic.active:
            raise Exception(f"Topic is not in ACTIVE state")

        message = Message(str(uuid.uuid4()), topic_id, content, int(time.time() * 1000))

        self.message_repository.save(message)

        threading.Thread(target=self.process_message_delivery_async, args=(message, topic)).start()


    def process_message_delivery_async(self, message: Message, topic: Topic):
        # Notify subscribers (always)
        topic.message_subject.notify(message)
        print(f"Background processing completed for message: {message.id}")
    