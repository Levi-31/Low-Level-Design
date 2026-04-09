

from enum import Enum


class Direction(Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    WEST = "WEST"
    SOUTH = "SOUTH"

    def __str__(self):
        return self.value
    
    