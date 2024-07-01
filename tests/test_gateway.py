"""
Gateway router test module.
"""

import os

from jupyterhub_ai_gateway.constants import gateway_route_paths
from jupyterhub_ai_gateway.routers.gateway import create_router


def test_gateway_router():
    """
    Test to ensure all gateway routes are in the router.

    Raises:
        AssertionError: If there are gateway routes that are not found in the router.
    """

    router = create_router(
        os.path.join(os.path.dirname(__file__), "data", "config.yaml")
    )

    gateway_paths = set(gateway_route_paths)
    route_paths = set(route.path for route in router.routes)

    missing_paths = gateway_paths - route_paths

    assert len(missing_paths) == 0
