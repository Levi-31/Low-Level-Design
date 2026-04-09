from domain.state.traffic_light_state import TrafficLightState


class GreenState(TrafficLightState):

    def turn_green(self, traffic_light):
        print(f"Traffic light {traffic_light.direction} is already Green")

    
    def turn_yellow(self, traffic_light):
        from domain.state.yellow_state import YellowState
        traffic_light.set_state(YellowState())

    
    def turn_red(self, traffic_light):
        from domain.state.red_state import RedState
        traffic_light.set_state(RedState())
        print(f"Traffic light {traffic_light.direction} changed from GREEN to RED")

    
    def turn_off(self, traffic_light):
        from domain.state.off_state import OffState
        traffic_light.set_state(OffState())
        print(f"Traffic light {traffic_light.direction} changed from Green to OFF")

    
    def get_state_name(self) -> str:
        return "GREEN"

    
    def can_transition_to(self, new_state) -> bool:
        from domain.state.red_state import RedState
        from domain.state.off_state import OffState
        return isinstance(new_state,(OffState,RedState))