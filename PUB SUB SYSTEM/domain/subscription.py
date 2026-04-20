


class Subscription:
    def __init__(self, id: str, topic_id: str, subscriber_id: str):
        self.id = id
        self.topic_id = topic_id
        self.subscriber_id = subscriber_id
        self.active = True
        self.created_at = 0
        