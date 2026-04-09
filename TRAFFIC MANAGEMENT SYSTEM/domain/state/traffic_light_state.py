


from abc import ABC, abstractmethod


class TrafficLightState(ABC):
    
    @abstractmethod
    def turn_green(self, traffic_light):
        pass

    @abstractmethod
    def turn_yellow(self, traffic_light):
        pass

    @abstractmethod
    def turn_red(self, traffic_light):
        pass

    @abstractmethod
    def turn_off(self, traffic_light):
        pass

    @abstractmethod
    def get_state_name(self) -> str:
        pass

    @abstractmethod
    def can_transition_to(self, new_state) -> bool:
        pass