"""
Gateway router module.
"""

import os

from fastapi import APIRouter, Security
from mlflow.deployments.server.app import create_app_from_path

from ..constants import gateway_route_paths
from ..security import get_current_user


def create_router(config_path: str) -> APIRouter:
    """
    Create gateway router.

    Paramaters:
        config_path (str): Path to configuration file.

    Returns:
        APIRouter: The router.
    """

    name = os.environ["JUPYTERHUB_SERVICE_NAME"]
    scopes = ["access:services", f"access:services!service={name}"]

    router = APIRouter(
        dependencies=[Security(get_current_user, scopes=scopes)],
    )

    app = create_app_from_path(config_path)

    for route in app.routes:
        if route.path in gateway_route_paths:
            router.add_api_route(
                route.path,
                route.endpoint,
                methods=route.methods,
            )

    return router