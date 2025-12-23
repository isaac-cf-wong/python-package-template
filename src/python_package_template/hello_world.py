"""Hello World Module."""

from __future__ import annotations


def say_hello(name: str) -> None:
    """Say Hello Function.

    Args:
        name: Name to greet.
    """
    print(f"Hello, {name}!")


def hello_world() -> None:
    """Hello World Function.

    Returns:
        A string output.
    """
    say_hello("world")


def good_night() -> str:
    """Good Night Function.

    Returns:
        A string output.
    """
    print("Good night!")
    return "string"


def hello_goodbye() -> None:
    """Hello Goodbye Function."""
    hello_world()
    good_night()
