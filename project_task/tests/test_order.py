"""Unit tests for Order module."""

import pytest

from src.order import Order, OrderStatus
from src.product import Product
from src.user import User


class TestOrder:
    """Test cases for Order class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.user = User("U001", "john_doe", "john@example.com")
        self.user.set_address("123 Main St")
        self.product1 = Product("P001", "Laptop", 999.99, 10)
        self.product2 = Product("P002", "Mouse", 29.99, 50)
        self.items = [(self.product1, 2), (self.product2, 1)]

    def test_order_creation(self):
        """Test creating an order."""
        order = Order("ORD-000001", self.user, self.items)
        assert order.order_id == "ORD-000001"
        assert order.user == self.user
        assert order.status == OrderStatus.PENDING
        assert len(order.items) == 2

    def test_order_empty_items(self):
        """Test that creating order with empty items raises ValueError."""
        with pytest.raises(ValueError):
            Order("ORD-000001", self.user, [])

    def test_order_total_price(self):
        """Test order total price calculation."""
        order = Order("ORD-000001", self.user, self.items)
        expected = (999.99 * 2) + (29.99 * 1)
        assert order.total_price == pytest.approx(expected)

    def test_update_order_status(self):
        """Test updating order status."""
        order = Order("ORD-000001", self.user, self.items)
        order.update_status(OrderStatus.CONFIRMED)
        assert order.status == OrderStatus.CONFIRMED

    def test_order_to_xml(self):
        """Test converting order to XML format."""
        order = Order("ORD-000001", self.user, self.items)
        xml_string = order.to_xml()

        # Check that XML contains expected elements
        assert "ORD-000001" in xml_string
        assert "john_doe" in xml_string
        assert "john@example.com" in xml_string
        assert "Laptop" in xml_string
        assert "Mouse" in xml_string
        assert "pending" in xml_string

    def test_order_xml_items(self):
        """Test that XML contains correct item information."""
        order = Order("ORD-000001", self.user, self.items)
        xml_string = order.to_xml()

        # Check quantities
        assert "2" in xml_string  # Laptop quantity
        assert "1" in xml_string  # Mouse quantity

    def test_order_repr(self):
        """Test order string representation."""
        order = Order("ORD-000001", self.user, self.items)
        repr_str = repr(order)
        assert "ORD-000001" in repr_str
        assert "john_doe" in repr_str
        assert "pending" in repr_str
