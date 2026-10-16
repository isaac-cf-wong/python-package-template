"""Top-level package for python_package_template."""

from __future__ import annotations

# PEP 810: defer importlib.metadata (loaded by version.py) on 3.15+.
# Ignored on 3.13/3.14 where the lazy import machinery does not exist.
__lazy_modules__ = ["python_package_template.version"]

from python_package_template.hello_world import goodbye_world, hello_goodbye, hello_world, say_goodbye, say_hello
from python_package_template.version import __version__

__all__ = ["__version__", "goodbye_world", "hello_goodbye", "hello_world", "say_goodbye", "say_hello"]
