"""Unit tests for User module."""

import pytest

from src.user import User


class TestUser:
    """Test cases for User class."""

    def test_user_creation(self):
        """Test creating a user."""
        user = User("U001", "john_doe", "john@example.com")
        assert user.user_id == "U001"
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.address is None

    def test_user_invalid_email(self):
        """Test that invalid email raises ValueError."""
        with pytest.raises(ValueError):
            User("U001", "john_doe", "invalid_email")

    def test_set_address(self):
        """Test setting user address."""
        user = User("U001", "john_doe", "john@example.com")
        user.set_address("123 Main St, City, Country")
        assert user.address == "123 Main St, City, Country"

    def test_set_empty_address(self):
        """Test that empty address raises ValueError."""
        user = User("U001", "john_doe", "john@example.com")
        with pytest.raises(ValueError):
            user.set_address("")

    def test_set_whitespace_address(self):
        """Test that whitespace-only address raises ValueError."""
        user = User("U001", "john_doe", "john@example.com")
        with pytest.raises(ValueError):
            user.set_address("   ")

    def test_user_repr(self):
        """Test user string representation."""
        user = User("U001", "john_doe", "john@example.com")
        assert "U001" in repr(user)
        assert "john_doe" in repr(user)
