import time

class IntersectionCycle:
    def __init__(self, intersection_id: int):
        self.intersection_id = intersection_id
        self.current_phase = 0  # 0=NORTH, 1=EAST, 2=SOUTH, 3=WEST
        self.is_paused = False
        self.paused_at_phase = 0
        self.phase_start_time = time.time()
        self.pause_start_time = 0.0
        self.total_pause_time = 0.0
        print(f"Intersection cycle created for intersection: {intersection_id}")

    def get_phase_elapsed_time(self) -> float:
        if self.is_paused:
            return self.pause_start_time - self.phase_start_time
        else:
            return time.time() - self.phase_start_time - self.total_pause_time

    def get_phase_remaining_time(self, phase_duration_seconds: int) -> float:
        elapsed = self.get_phase_elapsed_time()
        remaining = float(phase_duration_seconds) - elapsed
        return max(0.0, remaining)

    def get_total_pause_time(self) -> float:
        if self.is_paused:
            return self.total_pause_time + (time.time() - self.pause_start_time)
        return self.total_pause_time

    def set_current_phase(self, current_phase: int):
        self.current_phase = current_phase
        self.phase_start_time = time.time()
        self.total_pause_time = 0.0
        print(f"Phase changed to: {current_phase} for intersection {self.intersection_id}")

    def set_paused(self, paused: bool):
        if self.is_paused == paused:
            return
        self.is_paused = paused
        if paused:
            self.paused_at_phase = self.current_phase
            self.pause_start_time = time.time()
            print(f"Cycle paused at phase: {self.current_phase} (elapsed: {int(self.get_phase_elapsed_time())}s) for intersection {self.intersection_id}")
        else:
            self.total_pause_time += (time.time() - self.pause_start_time)
            print(f"Cycle resumed from phase: {self.paused_at_phase} (remaining: {int(self.get_phase_remaining_time(30))}s) for intersection {self.intersection_id}")

    def next_phase(self):
        self.current_phase = (self.current_phase + 1) % 4
        self.phase_start_time = time.time()
        self.total_pause_time = 0.0
        print(f"Advanced to next phase: {self.current_phase} for intersection {self.intersection_id}")

    def is_phase_complete(self, phase_duration_seconds: int) -> bool:
        return self.get_phase_elapsed_time() >= float(phase_duration_seconds)

    def __str__(self):
        return f"IntersectionCycle{{intersection_id={self.intersection_id}, current_phase={self.current_phase}, is_paused={self.is_paused}, phase_elapsed={int(self.get_phase_elapsed_time())}s}}"
