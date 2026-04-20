




import time

from controller.message_controller import MessageController
from controller.punlisher_controller import PublisherController
from controller.subscriber_controller import SubscriberController
from controller.susbcription_controller import SubscriptionController
from controller.topic_controller import TopicController
from repository.implementation.message_delivery_repo_implemetation import MessageDeliveryRepositoryImpl
from repository.implementation.message_repo_implementation import MessageRepositoryImpl
from repository.implementation.subscriber_repo_implementation import SubscriberRepositoryImpl
from repository.implementation.subscription_repo_implementation import SubscriptionRepositoryImpl
from repository.implementation.topic_repo_implementation import TopicRepositoryImpl
from service.message_service import MessageService
from service.publisher_service import PublisherService
from service.subscriber_service import SubscriberService
from service.subscription_service import SubscriptionService
from service.topic_service import TopicService


def main():
    print("=== PUB/SUB SYSTEM SIMULATION (Python) ===\n")

    # Initialize repositories
    topic_repository = TopicRepositoryImpl()
    subscriber_repository = SubscriberRepositoryImpl()
    message_repository = MessageRepositoryImpl()
    subscription_repository = SubscriptionRepositoryImpl()
    message_delivery_repository = MessageDeliveryRepositoryImpl()

    # Initialize services
    topic_service = TopicService(topic_repository)
    subscriber_service = SubscriberService(subscriber_repository, subscription_repository,
                                          message_delivery_repository, topic_repository)
    subscription_service = SubscriptionService(subscription_repository, subscriber_repository,
                                             topic_repository)
    publisher_service = PublisherService(topic_repository, message_repository,
                                        message_delivery_repository)
    message_service = MessageService(message_delivery_repository)

    # Initialize controllers
    topic_controller = TopicController(topic_service)
    subscriber_controller = SubscriberController(subscriber_service)
    subscription_controller = SubscriptionController(subscription_service)
    publisher_controller = PublisherController(publisher_service)
    message_controller = MessageController(message_service)

    import pdb;pdb.set_trace()
    # Simulation
    print("1. Creating topics...")
    tech_topic = topic_controller.create_topic("Technology")
    news_topic = topic_controller.create_topic("News")
    print("Created topics:")
    for topic in topic_controller.get_all_topics():
        print(f"  - {topic}")

    print("\n2. Registering subscribers...")
    alice = subscriber_controller.register_subscriber("alice@example.com")
    bob = subscriber_controller.register_subscriber("bob@example.com")
    print(f"Registered subscribers: {alice}, {bob}")

    print("\n3. Subscribing to topics...")
    subscription_controller.subscribe_to_topic(tech_topic.id, alice.id)
    subscription_controller.subscribe_to_topic(tech_topic.id, bob.id)
    subscription_controller.subscribe_to_topic(news_topic.id, alice.id)
    print("Subscriptions created")

    print("\n4. Publishing messages...")
    msg1 = publisher_controller.publish_message(tech_topic.id, "New AI breakthrough announced!")
    msg2 = publisher_controller.publish_message(news_topic.id, "Breaking: Major political update")
    print(f"Messages published:\n  - {msg1}\n  - {msg2}")

    print("\n5. Testing online/offline status...")
    subscriber_controller.go_online(alice.id, "conn-123")
    subscriber_controller.go_offline(bob.id)
    print("Status changes applied")

    print("\n6. Publishing another message...")
    msg3 = publisher_controller.publish_message(tech_topic.id, "Tech conference next week!")
    print(f"Message published: {msg3}")

    print("\n7. Acknowledging message...")
    # message_controller.acknowledge_message(msg1.id, alice.id)
    print("Message acknowledged")

    # Small delay to allow background threads to finish output
    time.sleep(0.5)

    print("\n=== SIMULATION COMPLETED ===")

if __name__ == "__main__":
    main()
