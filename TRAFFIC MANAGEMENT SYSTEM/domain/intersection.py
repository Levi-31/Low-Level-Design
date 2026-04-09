from typing import Dict, Optional

from domain.direction import Direction
from domain.traffic_light import TrafficLight


class Intersection:
    def __init__(self,id:int,name:str):
        self.id = id
        self.name = name
        is_emergency_mode = False
        is_cycle_paused = False
        emergency_direction : Optional[Direction] = None
        self.traffic_lights: Dict[Direction, TrafficLight] = {
            dir: TrafficLight(dir) for dir in Direction
        }


    def set_emergency_mode(self, emergency_mode: bool):
        self.is_emergency_mode = emergency_mode
        print(f"Emergency mode {'enabled' if emergency_mode else 'disabled'} for intersection {self.id}")


    def set_emergency_direction(self, emergency_direction: Direction):
        self.emergency_direction = emergency_direction
        print(f"Emergency direction set to: {emergency_direction} for intersection {self.id}")

    def set_cycle_paused(self, cycle_paused: bool):
        self.is_cycle_paused = cycle_paused
        print(f"Cycle {'paused' if cycle_paused else 'resumed'} for intersection {self.id}")

    def get_traffic_light(self, direction: Direction) -> Optional[TrafficLight]:
        return self.traffic_lights.get(direction)
    
    def set_all_signals_to_red(self):
        for light in self.traffic_lights.values():
            current_state = light.get_current_state_name()
            if current_state == "GREEN":
                light.turn_yellow()
                light.turn_red()
            elif current_state == "YELLOW":
                light.turn_red()
            elif current_state != "RED":
                light.turn_red()
            else:
                print(f"Traffic light {light.direction} is already RED")
        print(f"All signals set to RED for intersection {self.id}")

    def set_signal_to_green(self, direction: Direction):
        light = self.get_traffic_light(direction)
        if light:
            light.turn_green()
            print(f"Signal {direction} set to GREEN for intersection {self.id}")
    

    def set_signal_to_yellow(self, direction: Direction):
        light = self.get_traffic_light(direction)
        if light:
            light.turn_yellow()
            print(f"Signal {direction} set to YELLOW for intersection {self.id}")

    def set_signal_to_red(self, direction: Direction):
        light = self.get_traffic_light(direction)
        if light:
            light.turn_red()
            print(f"Signal {direction} set to RED for intersection {self.id}")


    def set_signal_to_off(self, direction: Direction):
        light = self.get_traffic_light(direction)
        if light:
            light.turn_off()
            print(f"Signal {direction} set to OFF for intersection {self.id}")

    def emergency_transition_to_red(self, direction: Direction):
        light = self.get_traffic_light(direction)
        if light:
            current_state = light.get_current_state_name()
            if current_state == "GREEN":
                print(f"Emergency transition: {direction} GREEN → YELLOW → RED")
                light.turn_yellow()
                light.turn_red()
            elif current_state == "YELLOW":
                print(f"Emergency transition: {direction} YELLOW → RED")
                light.turn_red()
            elif current_state == "RED":
                print(f"Emergency transition: {direction} already RED")
            else:
                print(f"Emergency transition: {direction} → RED")
                light.turn_red()
