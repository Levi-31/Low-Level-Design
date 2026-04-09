import time

from domain.direction import Direction


class VehicleCounter:
    def __init__(self, direction: Direction):
        self.direction = direction
        self.count = 0
        self.last_update = time.time()
        print(f"Vehicle counter created for direction: {direction}")

    def update_count(self, count: int):
        self.count = count
        self.last_update = time.time()
        print(f"Vehicle count updated for {self.direction}: {count}")

    def reset_count(self):
        self.count = 0
        self.last_update = time.time()
        print(f"Vehicle count reset for {self.direction}")

    def __str__(self):
        return f"VehicleCounter{{direction={self.direction}, count={self.count}}}"
