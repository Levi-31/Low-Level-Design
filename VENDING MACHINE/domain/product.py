

class Product:
    def __init__(self,id:int ,name:str, price:float, category:ProductCategory):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
    

    def __str__(self):
        return f"{self.name} - ${self.price}"