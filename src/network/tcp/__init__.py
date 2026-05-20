"""Simple TCP server/client utilities for unit testing.

This package provides a small, dependency-free TCP server and client
implementation used by unit tests. Keep implementations lightweight and
rely only on the Python standard library so tests are fast and hermetic.
"""

from .server import TCPServer
from .client import TCPClient

__all__ = ["TCPServer", "TCPClient"]

