"""Unit tests for Product module."""

import pytest

from src.product import Product

class TestProduct:
    """Test cases for Product class."""

    def test_product_creation(self):
        """Test creating a product."""
        product = Product("P001", "Laptop", 999.99, 10)
        assert product.product_id == "P001"
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.stock == 10

    def test_product_negative_price(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError):
            Product("P001", "Laptop", -100, 10)

    def test_product_negative_stock(self):
        """Test that negative stock raises ValueError."""
        with pytest.raises(ValueError):
            Product("P001", "Laptop", 999.99, -5)

    def test_decrease_stock_successful(self):
        """Test successful stock decrease."""
        product = Product("P001", "Laptop", 999.99, 10)
        assert product.decrease_stock(3) is True
        assert product.stock == 7

    def test_decrease_stock_insufficient(self):
        """Test stock decrease with insufficient stock."""
        product = Product("P001", "Laptop", 999.99, 5)
        assert product.decrease_stock(10) is False
        assert product.stock == 5

    def test_increase_stock(self):
        """Test stock increase."""
        product = Product("P001", "Laptop", 999.99, 10)
        product.increase_stock(5)
        assert product.stock == 15

    def test_increase_stock_negative_quantity(self):
        """Test that negative quantity raises ValueError."""
        product = Product("P001", "Laptop", 999.99, 10)
        with pytest.raises(ValueError):
            product.increase_stock(-5)

    def test_product_repr(self):
        """Test product string representation."""
        product = Product("P001", "Laptop", 999.99, 10)
        assert "P001" in repr(product)
        assert "Laptop" in repr(product)
