

from datetime import datetime

from domain.observer.message_subject import MessageSubject


class Topic:
    def __init__(self,id:str , name : str):
        self.id = id
        self.name = name
        self.active = True
        self.created_at = 0
        self.message_subject = MessageSubject()
    

    def __str__(self):
        return f"Topic{{id='{self.id}', name='{self.name}', isActive={str(self.active).lower()}, emailSubscribers={len(self.message_subject.email_subscribers)}, realtimeSubscribers={len(self.message_subject.realtime_subscribers)}}}"

