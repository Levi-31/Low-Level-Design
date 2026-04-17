from enum import Enum

class ProductCategory(Enum):
    BEVERAGE = "BEVERAGE"
    CHIPS = "CHIPS"
    CANDY = "CANDY"
    COOKIES = "COOKIES"
    SNACK = "SNACK"

    def __str__(self):
        return self.value
