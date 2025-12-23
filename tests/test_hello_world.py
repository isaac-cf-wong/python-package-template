"""Sample tests for hello_world module."""

from __future__ import annotations

from python_package_template.hello_world import good_night, hello_goodbye, hello_world, say_hello


def test_say_hello(capsys, some_name):
    """
    Test say_hello function.
    It uses the some_name fixture defined in conftest.py.

    Args:
        capsys: Pytest fixture to capture stdout and stderr.
        some_name: A string input from fixture.
    """
    say_hello(some_name)
    captured = capsys.readouterr()
    assert captured.out == f"Hello, {some_name}!\n"


def test_hello_world(capsys):
    """
    Test hello_world function.
    It uses the some_integer fixture defined in conftest.py.

    Args:
        capsys: Pytest fixture to capture stdout and stderr.
        some_integer: An integer input from fixture.
    """
    hello_world()
    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\n"


def test_good_night(capsys):
    assert good_night() == "string"
    captured = capsys.readouterr()
    assert captured.out == "Good night!\n"


def test_hello_goodbye(capsys):
    hello_goodbye()
    captured = capsys.readouterr()
    assert captured.out == "Hello, world!\nGood night!\n"
