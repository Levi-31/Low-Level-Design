import time

from domain.direction import Direction

class EmergencyRequest:
    def __init__(self, id: int, intersection_id: int, direction: Direction, duration: int):
        self.id = id
        self.intersection_id = intersection_id
        self.direction = direction
        self.duration = duration
        self.is_active = True
        self.request_time = time.time()
        print(f"Emergency request created: ID={id}, Intersection={intersection_id}, "
              f"Direction={direction}, Duration={duration}s")

    def set_active(self, active: bool):
        self.is_active = active
        print(f"Emergency request {self.id} {'activated' if active else 'deactivated'}")

    def is_expired(self) -> bool:
        elapsed_time = time.time() - self.request_time
        return elapsed_time >= self.duration

    def __str__(self):
        return f"EmergencyRequest{{id={self.id}, intersection_id={self.intersection_id}, " \
               f"direction={self.direction}, duration={self.duration}, is_active={self.is_active}, " \
               f"request_time={self.request_time}}}"
