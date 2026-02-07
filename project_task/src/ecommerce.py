from typing import Dict, List, Optional
from cart import Cart
from order import Order, OrderStatus
from product import Product
from user import User

class ECommercePlatform:
    def __init__(self):
        self._products: Dict[str, Product] = {}
        self._users: Dict[str, User] = {}
        self._carts: Dict[str, Cart] = {}
        self._orders: Dict[str, Order] = {}
        self._order_counter = 0

    def register_product(self, product: Product) -> bool:
        if product.product_id in self._products:
            return False
        self._products[product.product_id] = product
        return True

    def register_user(self, user: User) -> bool:
        if user.user_id in self._users:
            return False
        self._users[user.user_id] = user
        self._carts[user.user_id] = Cart(user.user_id)
        return True

    def get_product(self, product_id: str) -> Optional[Product]:
        return self._products.get(product_id)

    def get_user(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def get_cart(self, user_id: str) -> Optional[Cart]:
        return self._carts.get(user_id)

    def add_to_cart(
        self, user_id: str, product_id: str, quantity: int
    ) -> bool:
        cart = self._carts.get(user_id)
        if not cart:
            return False

        product = self._products.get(product_id)
        if not product:
            return False

        return cart.add_item(product, quantity)

    def remove_from_cart(self, user_id: str, product_id: str) -> bool:
        cart = self._carts.get(user_id)
        if not cart:
            return False
        return cart.remove_item(product_id)

    def checkout(self, user_id: str) -> Optional[Order]:
        user = self._users.get(user_id)
        cart = self._carts.get(user_id)

        if not user or not cart or cart.is_empty():
            return None

        if not user.address:
            return None

        self._order_counter += 1
        order_id = f"ORD-{self._order_counter:06d}"
        order = Order(order_id, user, cart.get_items())

        for product, quantity in order.items:
            product.decrease_stock(quantity)

        self._orders[order_id] = order

        cart.clear()

        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def update_order_status(
        self, order_id: str, new_status: OrderStatus
    ) -> bool:
        order = self._orders.get(order_id)

        if not order:
            return False
        order.update_status(new_status)
        
        return True

    def get_user_orders(self, user_id: str) -> List[Order]:
        return [order for order in self._orders.values()
                if order.user.user_id == user_id]

    def get_all_products(self) -> List[Product]:
        return list(self._products.values())

    def get_all_orders(self) -> List[Order]:
        return list(self._orders.values())
