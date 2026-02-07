"""Unit tests for Cart module."""

import pytest

from src.cart import Cart
from src.product import Product


class TestCart:
    """Test cases for Cart class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cart = Cart("U001")
        self.product1 = Product("P001", "Laptop", 999.99, 10)
        self.product2 = Product("P002", "Mouse", 29.99, 50)

    def test_cart_creation(self):
        """Test creating a cart."""
        assert self.cart.user_id == "U001"
        assert self.cart.is_empty() is True

    def test_add_item_to_cart(self):
        """Test adding item to cart."""
        assert self.cart.add_item(self.product1, 2) is True
        items = self.cart.get_items()
        assert len(items) == 1
        assert items[0][1] == 2

    def test_add_item_insufficient_stock(self):
        """Test adding item with insufficient stock."""
        assert self.cart.add_item(self.product1, 15) is False
        assert self.cart.is_empty() is True

    def test_add_multiple_items(self):
        """Test adding multiple items to cart."""
        self.cart.add_item(self.product1, 1)
        self.cart.add_item(self.product2, 3)
        items = self.cart.get_items()
        assert len(items) == 2

    def test_add_same_item_twice(self):
        """Test adding same item twice (should increase quantity)."""
        self.cart.add_item(self.product1, 2)
        self.cart.add_item(self.product1, 3)
        items = self.cart.get_items()
        assert len(items) == 1
        assert items[0][1] == 5

    def test_add_item_invalid_quantity(self):
        """Test adding item with invalid quantity."""
        with pytest.raises(ValueError):
            self.cart.add_item(self.product1, 0)
        with pytest.raises(ValueError):
            self.cart.add_item(self.product1, -5)

    def test_remove_item_from_cart(self):
        """Test removing item from cart."""
        self.cart.add_item(self.product1, 2)
        assert self.cart.remove_item("P001") is True
        assert self.cart.is_empty() is True

    def test_remove_nonexistent_item(self):
        """Test removing non-existent item."""
        assert self.cart.remove_item("P999") is False

    def test_update_quantity(self):
        """Test updating item quantity."""
        self.cart.add_item(self.product1, 2)
        assert self.cart.update_quantity("P001", 5) is True
        items = self.cart.get_items()
        assert items[0][1] == 5

    def test_update_quantity_to_zero(self):
        """Test updating quantity to zero (removes item)."""
        self.cart.add_item(self.product1, 2)
        assert self.cart.update_quantity("P001", 0) is True
        assert self.cart.is_empty() is True

    def test_update_quantity_insufficient_stock(self):
        """Test updating to quantity larger than stock."""
        self.cart.add_item(self.product1, 2)
        assert self.cart.update_quantity("P001", 15) is False

    def test_get_total_price(self):
        """Test calculating total cart price."""
        self.cart.add_item(self.product1, 2)
        self.cart.add_item(self.product2, 1)
        total = self.cart.get_total_price()
        expected = (999.99 * 2) + (29.99 * 1)
        assert total == pytest.approx(expected)

    def test_clear_cart(self):
        """Test clearing cart."""
        self.cart.add_item(self.product1, 2)
        self.cart.add_item(self.product2, 1)
        self.cart.clear()
        assert self.cart.is_empty() is True

    def test_cart_repr(self):
        """Test cart string representation."""
        self.cart.add_item(self.product1, 2)
        repr_str = repr(self.cart)
        assert "U001" in repr_str
        assert "items=1" in repr_str
