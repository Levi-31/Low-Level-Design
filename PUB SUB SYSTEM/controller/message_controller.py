


from service.message_service import MessageService


class MessageController:
    def __init__(self, message_service: MessageService):
        self.message_service = message_service

    def acknowledge_message(self, message_id: str, subscriber_id: str):
        self.message_service.acknowledge_message(message_id, subscriber_id)