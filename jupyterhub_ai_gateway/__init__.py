"""
Package main module.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("jupyterhub-ai-gateway")
except PackageNotFoundError:
    pass
