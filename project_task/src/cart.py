from typing import Dict, List, Tuple
from product import Product

class Cart:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self._items: Dict[str, Tuple[Product, int]] = {}

    def add_item(self, product: Product, quantity: int) -> bool:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if product.product_id in self._items:
            current_product, current_qty = self._items[product.product_id]
            new_quantity = current_qty + quantity
            if new_quantity > product.stock:
                return False
            self._items[product.product_id] = (product, new_quantity)
        else:
            if quantity > product.stock:
                return False
            self._items[product.product_id] = (product, quantity)

        return True

    def remove_item(self, product_id: str) -> bool:
        if product_id not in self._items:
            return False
        del self._items[product_id]
        return True

    def update_quantity(self, product_id: str, quantity: int) -> bool:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        if product_id not in self._items:
            return False

        if quantity == 0:
            del self._items[product_id]
            return True

        product, _ = self._items[product_id]
        if quantity > product.stock:
            return False

        self._items[product_id] = (product, quantity)
        return True

    def get_items(self) -> List[Tuple[Product, int]]:
        return list(self._items.values())

    def get_total_price(self) -> float:
        total = sum(
            product.price * quantity
            for product, quantity in self._items.values()
        )
        return total

    def clear(self) -> None:
        self._items.clear()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __repr__(self) -> str:
        item_count = len(self._items)
        total = self.get_total_price()
        return (
            f"Cart(user_id={self.user_id}, "
            f"items={item_count}, total={total})"
        )
