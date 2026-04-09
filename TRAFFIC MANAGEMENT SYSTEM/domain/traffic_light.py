

from domain.direction import Direction
from domain.state.red_state import RedState


class TrafficLight:
    def __init__(self,direction:Direction):
        self.direction = direction
        self.current_state = RedState()
        print(f"Traffic light created for direction: {direction} in RED state")
    
    def set_state(self, new_state):
        self.current_state = new_state

    def turn_green(self):
        self.current_state.turn_green(self)

    def turn_yellow(self):
        self.current_state.turn_yellow(self)

    def turn_red(self):
        self.current_state.turn_red(self)

    def turn_off(self):
        self.current_state.turn_off(self)

    def get_current_state_name(self) -> str:
        return self.current_state.get_state_name()

    def can_transition_to(self, new_state) -> bool:
        return self.current_state.can_transition_to(new_state)