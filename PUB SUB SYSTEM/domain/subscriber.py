


class Subscriber:
    def __init__(self, id: str, email: str):
        self.id = id
        self.email = email
        self.realtime_connection_id = None
        self.is_online = True
        self.created_at = 0
        self.last_heartbeat = 0

    def __str__(self):
        return f"Subscriber{{id='{self.id}', email='{self.email}', isOnline={str(self.is_online).lower()}}}"