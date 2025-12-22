"""
Configuration and fixtures for pytest.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def some_integer() -> int:
    """A simple fixture that provides an integer value for testing.

    Returns:
        An integer value.
    """
    return 42
