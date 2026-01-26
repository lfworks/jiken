"""Core module for the Python project template."""


def greet(name: str) -> str:
    """Greet a person by name.

    Args:
        name: The name of the person to greet.

    Returns:
        A greeting message.

    Examples:
        >>> greet("World")
        'Hello, World!'
    """
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of a and b.

    Examples:
        >>> add(2, 3)
        5
    """
    return a + b
