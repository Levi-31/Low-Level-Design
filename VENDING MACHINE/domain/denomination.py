

from enum import Enum


class Denomination(Enum):
    ONE_DOLLAR = 100
    FIVE_DOLLAR = 500
    TEN_DOLLAR = 1000
    TWENTY_DOLLAR = 2000
    FIFTY_DOLLAR = 5000
    HUNDRED_DOLLAR = 10000

    @property
    def value_in_dollars(self):
        return self.value / 100.0

    def __str__(self):
        return self.name