"""Tests for the core module."""

import pytest  # noqa: F401

from python_project_template.core import add, greet


def test_greet() -> None:
    """Test the greet function."""
    assert greet("World") == "Hello, World!"
    assert greet("Alice") == "Hello, Alice!"


def test_greet_empty_string() -> None:
    """Test greet with an empty string."""
    assert greet("") == "Hello, !"


def test_add() -> None:
    """Test the add function."""
    assert add(2, 3) == 5
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    assert add(100, 200) == 300


def test_add_negative_numbers() -> None:
    """Test add with negative numbers."""
    assert add(-5, -3) == -8
    assert add(-10, 5) == -5
