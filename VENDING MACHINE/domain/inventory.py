class Inventory:
    def __init__(self,product_id:int, vending_machine_id: int, quantity:int, min_threshold:int):
        self.product_id = product_id
        self.vending_machine_id = vending_machine_id
        self.quantity = quantity
        self.min_threshold = min_threshold
    

    def is_low_stock(self) -> bool:
        return self.quantity <= self.min_threshold
    
    def is_out_of_stock(self) -> bool:
        return self.quantity <= 0
    
    def add_quantity(self, no_of_items: int):
        self.quantity += no_of_items

    def remove_quantity(self, no_of_items: int):
        if self.quantity >= no_of_items:
            self.quantity -= no_of_items
        else:
            self.quantity = 0


    def __str__(self):
        return f"Product {self.product_id} - Quantity: {self.quantity} (Min: {self.min_threshold})"