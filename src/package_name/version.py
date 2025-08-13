"""
A script to infer the version number from the metadata.
"""

from __future__ import annotations

from importlib.metadata import version

__version__ = version("package_name")
