

from domain.tier import UserTier


class User:
    def __init__(self, user_id: str, tier: UserTier):
        self.user_id = user_id
        self.tier = tier