


from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    CUSTOMER = "CUSTOMER"

    def __str__(self):
        return self.value