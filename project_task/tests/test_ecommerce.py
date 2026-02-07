"""Unit tests for E-Commerce Platform module."""

import pytest

from src.ecommerce import ECommercePlatform
from src.order import OrderStatus
from src.product import Product
from src.user import User

class TestECommercePlatform:
    """Test cases for ECommercePlatform class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.platform = ECommercePlatform()
        self.product1 = Product("P001", "Laptop", 999.99, 10)
        self.product2 = Product("P002", "Mouse", 29.99, 50)
        self.user = User("U001", "john_doe", "john@example.com")

    def test_platform_creation(self):
        """Test creating a platform."""
        assert len(self.platform.get_all_products()) == 0
        assert len(self.platform.get_all_orders()) == 0

    def test_register_product(self):
        """Test registering a product."""
        assert self.platform.register_product(self.product1) is True
        products = self.platform.get_all_products()
        assert len(products) == 1

    def test_register_duplicate_product(self):
        """Test registering duplicate product."""
        self.platform.register_product(self.product1)
        assert self.platform.register_product(self.product1) is False

    def test_get_product(self):
        """Test getting a product."""
        self.platform.register_product(self.product1)
        product = self.platform.get_product("P001")
        assert product is not None
        assert product.name == "Laptop"

    def test_get_nonexistent_product(self):
        """Test getting non-existent product."""
        assert self.platform.get_product("P999") is None

    def test_register_user(self):
        """Test registering a user."""
        assert self.platform.register_user(self.user) is True
        user = self.platform.get_user("U001")
        assert user is not None

    def test_register_duplicate_user(self):
        """Test registering duplicate user."""
        self.platform.register_user(self.user)
        assert self.platform.register_user(self.user) is False

    def test_get_user(self):
        """Test getting a user."""
        self.platform.register_user(self.user)
        user = self.platform.get_user("U001")
        assert user is not None
        assert user.username == "john_doe"

    def test_get_cart_for_user(self):
        """Test getting cart for a user."""
        self.platform.register_user(self.user)
        cart = self.platform.get_cart("U001")
        assert cart is not None
        assert cart.is_empty() is True

    def test_add_to_cart(self):
        """Test adding item to cart."""
        self.platform.register_product(self.product1)
        self.platform.register_user(self.user)
        assert self.platform.add_to_cart("U001", "P001", 2) is True

    def test_add_to_cart_invalid_user(self):
        """Test adding to cart for non-existent user."""
        self.platform.register_product(self.product1)
        assert self.platform.add_to_cart("U999", "P001", 2) is False

    def test_add_to_cart_invalid_product(self):
        """Test adding non-existent product to cart."""
        self.platform.register_user(self.user)
        assert self.platform.add_to_cart("U001", "P999", 2) is False

    def test_remove_from_cart(self):
        """Test removing item from cart."""
        self.platform.register_product(self.product1)
        self.platform.register_user(self.user)
        self.platform.add_to_cart("U001", "P001", 2)
        assert self.platform.remove_from_cart("U001", "P001") is True

    def test_checkout_successful(self):
        """Test successful checkout."""
        self.platform.register_product(self.product1)
        self.platform.register_user(self.user)
        self.user.set_address("123 Main St")

        self.platform.add_to_cart("U001", "P001", 2)
        order = self.platform.checkout("U001")

        assert order is not None
        assert order.order_id == "ORD-000001"
        assert len(order.items) == 1
        assert order.items[0][1] == 2  # quantity is 2

    def test_checkout_without_address(self):
        """Test checkout fails without address."""
        self.platform.register_product(self.product1)
        self.platform.register_user(self.user)
        # Don't set address

        self.platform.add_to_cart("U001", "P001", 2)
        order = self.platform.checkout("U001")

        assert order is None

    def test_checkout_empty_cart(self):
        """Test checkout with empty cart."""
        self.platform.register_user(self.user)
        self.user.set_address("123 Main St")
        order = self.platform.checkout("U001")
        assert order is None

    def test_stock_decreased_after_checkout(self):
        """Test that stock is decreased after checkout."""
        self.platform.register_product(self.product1)
        self.platform.register_user(self.user)
        self.user.set_address("123 Main St")

        initial_stock = self.product1.stock
        self.platform.add_to_cart("U001", "P001", 2)
        self.platform.checkout("U001")

        assert self.product1.stock == initial_stock - 2

    def test_cart_cleared_after_checkout(self):
        """Test that cart is cleared after checkout."""
        self.platform.register_product(self.product1)
        self.platform.register_user(self.user)
        self.user.set_address("123 Main St")

        self.platform.add_to_cart("U001", "P001", 2)
        self.platform.checkout("U001")

        cart = self.platform.get_cart("U001")
        assert cart.is_empty() is True

    def test_get_order(self):
        """Test getting an order."""
        self.platform.register_product(self.product1)
        self.platform.register_user(self.user)
        self.user.set_address("123 Main St")

        self.platform.add_to_cart("U001", "P001", 2)
        order = self.platform.checkout("U001")

        retrieved_order = self.platform.get_order(order.order_id)
        assert retrieved_order is not None
        assert retrieved_order.order_id == order.order_id

    def test_update_order_status(self):
        """Test updating order status."""
        self.platform.register_product(self.product1)
        self.platform.register_user(self.user)
        self.user.set_address("123 Main St")

        self.platform.add_to_cart("U001", "P001", 2)
        order = self.platform.checkout("U001")

        assert self.platform.update_order_status(
            order.order_id, OrderStatus.SHIPPED
        ) is True
        assert order.status == OrderStatus.SHIPPED

    def test_get_user_orders(self):
        """Test getting all orders for a user."""
        self.platform.register_product(self.product1)
        self.platform.register_user(self.user)
        self.user.set_address("123 Main St")

        # Create two orders
        self.platform.add_to_cart("U001", "P001", 1)
        self.platform.checkout("U001")

        self.platform.add_to_cart("U001", "P001", 1)
        self.platform.checkout("U001")

        orders = self.platform.get_user_orders("U001")
        assert len(orders) == 2
