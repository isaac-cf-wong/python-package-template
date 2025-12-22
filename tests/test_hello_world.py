"""Sample tests for hello_world module."""

from __future__ import annotations

from python_package_template.hello_world import good_night, hello_goodbye, hello_world


def test_hello_world(capsys, some_integer: int):
    """
    Test hello_world function.
    It uses the some_integer fixture defined in conftest.py.

    Args:
        capsys: Pytest fixture to capture stdout and stderr.
        some_integer: An integer input from fixture.
    """
    assert hello_world(some_integer) == f"string-{some_integer}"
    assert capsys.readouterr().out == "hello world\n"


def test_good_night(capsys):
    assert good_night() == "string"
    captured = capsys.readouterr()
    assert captured.out == "good night\n"


def test_hello_goodbye(capsys):
    hello_goodbye()
    captured = capsys.readouterr()
    assert captured.out == "hello world\ngood night\n"
