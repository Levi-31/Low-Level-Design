


from dataclasses import dataclass

@dataclass
class Message:
    id: str
    topic_id: str
    content: str
    timestamp: int

    def __str__(self):
        return f"Message{{id='{self.id}', topicId='{self.topic_id}', content='{self.content}', timestamp={self.timestamp}}}"
