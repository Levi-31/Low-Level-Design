


from domain.state.invalid_state_transition import InvalidStateTransitionException

from domain.state.traffic_light_state import TrafficLightState


class RedState(TrafficLightState):

    def turn_green(self, traffic_light):
        from domain.state.green_state import GreenState
        traffic_light.set_state(GreenState())
        print(f"Traffic light {traffic_light.direction} changed from RED to GREEN")


    def turn_yellow(self, traffic_light):
        raise InvalidStateTransitionException("RED", "YELLOW")
    
    def turn_red(self, traffic_light):
        print(f"Traffic light {traffic_light.direction} is already RED")

    def turn_off(self, traffic_light):
        from domain.state.off_state import OffState
        traffic_light.set_state(OffState())
        print(f"Traffic light {traffic_light.direction} changed from RED to OFF")

    def get_state_name(self) -> str:
        return "RED"
    
    def can_transition_to(self, new_state) -> bool:
        from domain.state.off_state import OffState
        from domain.state.green_state import GreenState
        return isinstance(new_state, (GreenState, OffState))