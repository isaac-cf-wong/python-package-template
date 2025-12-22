"""Hello World Module."""

from __future__ import annotations


def hello_world(i: int = 0) -> str:
    """Hello World Function.

    Args:
        i: An integer input.

    Returns:
        A string output.
    """
    print("hello world")
    return f"string-{i}"


def good_night() -> str:
    """Good Night Function.

    Returns:
        A string output.
    """
    print("good night")
    return "string"


def hello_goodbye() -> None:
    """Hello Goodbye Function."""
    hello_world(1)
    good_night()
