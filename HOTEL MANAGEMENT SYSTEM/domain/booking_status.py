


from enum import Enum

class BookingStatus(Enum):
    CREATED = "CREATED"
    HELD = "HELD"
    CONFIRMED = "CONFIRMED"
    CHECKED_IN = "CHECKED_IN"
    CHECKED_OUT = "CHECKED_OUT"
    CANCELLED = "CANCELLED"

    def __str__(self):
        return self.value