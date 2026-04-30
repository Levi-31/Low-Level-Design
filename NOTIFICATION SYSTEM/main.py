


from controller.notification_controller import NotificationController
from domain.notification_channel import NotificationChannel
from domain.subscriber import Subscriber
from repository.notification_repository import NotificationRepository
from service.notification_service import NotificationService
from service.observer.notification_observer import Logger, NotificationEngine, NotificationObservable
from service.strategy.notification_strategy import EmailStrategy, PushStrategy, SMSStrategy


if __name__ == "__main__":
    observable = NotificationObservable()

    logger = Logger()
    engine = NotificationEngine([
        EmailStrategy(),
        SMSStrategy(),
        PushStrategy()
    ])

    observable.add(logger)
    observable.add(engine)

    repo = NotificationRepository()
    service = NotificationService(repo, observable)
    controller = NotificationController(service)

    
    users = [
        Subscriber("user1", [NotificationChannel.EMAIL]),
        Subscriber("user2", [NotificationChannel.SMS, NotificationChannel.PUSH]),
        Subscriber("user3", [NotificationChannel.PUSH]),
    ]
    
    controller.send_notification("Hello from system",users)