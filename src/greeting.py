"""Greeting function module.

This module provides a simple, reusable function that generates personalized
greeting messages or returns a default greeting when no name is provided.

The greeting() function supports flexible input handling, including None values,
various data types, and whitespace normalization.
"""

from typing import Optional, Any


def greeting(name: Optional[Any] = None) -> str:
    """Generate a personalized or default greeting message.

    Returns a friendly greeting message. If no name is provided or the provided
    input is empty after processing, returns a default greeting. Otherwise,
    returns a personalized greeting with the provided name.

    The function accepts any type of input and converts it to a string for
    processing. Empty strings and whitespace-only strings are treated as
    "no name provided" and result in the default greeting.

    Args:
        name (Optional[Any]): The name to greet. Can be None, a string, or
            any other type that can be converted to a string. Non-string types
            are converted using Python's str() function. Empty strings and
            strings containing only whitespace are treated as None.
            Defaults to None.

    Returns:
        str: A greeting message in one of two formats:
            - "Hello, World!" if no name is provided or name is empty/whitespace
            - "Hello, {name}!" where {name} is the provided (or converted) name
              with leading/trailing whitespace removed.

    Examples:
        >>> greeting()
        'Hello, World!'
        >>> greeting(None)
        'Hello, World!'
        >>> greeting("Alice")
        'Hello, Alice!'
        >>> greeting("  Bob  ")
        'Hello, Bob!'
        >>> greeting("")
        'Hello, World!'
        >>> greeting("   ")
        'Hello, World!'
        >>> greeting(123)
        'Hello, 123!'
        >>> greeting(3.14)
        'Hello, 3.14!'
    """
    # Step 1: Check if name is None
    if name is None:
        return "Hello, World!"

    # Step 2: Convert name to string
    try:
        string_name = str(name)
    except Exception:
        # Graceful degradation: if str() conversion fails, return default
        return "Hello, World!"

    # Step 3: Strip leading/trailing whitespace
    stripped_name = string_name.strip()

    # Step 4: Check if stripped_name is empty
    if not stripped_name:
        return "Hello, World!"

    # Step 5: Return formatted greeting
    return f"Hello, {stripped_name}!"
