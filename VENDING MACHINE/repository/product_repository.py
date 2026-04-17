from typing import Dict, Optional
from domain.product import Product

class ProductRepository:
    def __init__(self):
        self._products: Dict[int, Product] = {}

    def save(self, product: Product):
        self._products[product.id] = product

    def find_by_id(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)
