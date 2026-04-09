

from domain.state.invalid_state_transition import InvalidStateTransitionException
from domain.state.traffic_light_state import TrafficLightState


class YellowState(TrafficLightState):
    def turn_green(self, traffic_light):
        raise InvalidStateTransitionException("YELLOW", "GREEN")

    def turn_yellow(self, traffic_light):
        print(f"Traffic light {traffic_light.direction} is already YELLOW")

    def turn_red(self, traffic_light):
        from domain.state.red_state import RedState
        traffic_light.set_state(RedState())
        print(f"Traffic light {traffic_light.direction} changed from YELLOW to RED")

    def turn_off(self, traffic_light):
        from domain.state.off_state import OffState
        traffic_light.set_state(OffState())
        print(f"Traffic light {traffic_light.direction} changed from YELLOW to OFF")

    def get_state_name(self) -> str:
        return "YELLOW"

    def can_transition_to(self, new_state) -> bool:
        from domain.state.red_state import RedState
        from domain.state.off_state import OffState
        return isinstance(new_state, (RedState, OffState))
