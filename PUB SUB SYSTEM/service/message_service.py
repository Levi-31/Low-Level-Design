


from repository.message_delivery_repository import MessageDeliveryRepository


class MessageService:
    def __init__(self, message_delivery_repository: MessageDeliveryRepository):
        self.message_delivery_repository = message_delivery_repository

    def acknowledge_message(self, message_id: str, subscriber_id: str):
        # Implementation for acknowledging message...
        print(f"Acknowledged message {message_id} by subscriber {subscriber_id}")