"""
Gateway router module.
"""

from fastapi import APIRouter, Security
from mlflow.deployments.server.app import create_app_from_path

from ..constants import gateway_routes
from ..security import get_current_user
from ..settings import settings


def create_router(config_path: str) -> APIRouter:
    """
    Create gateway router.

    Paramaters:
        config_path (str): Path to configuration file.

    Returns:
        APIRouter: The router.
    """

    scopes = [
        "access:services",
        f"access:services!service={settings.jupyterhub_service_name}",
    ]

    router = APIRouter(
        dependencies=[Security(get_current_user, scopes=scopes)],
    )

    app = create_app_from_path(config_path)

    routes = {
        (("path", route.path), ("methods", tuple(route.methods))): route
        for route in app.routes
    }

    for gateway_route in gateway_routes:
        route = routes.get(tuple(gateway_route.items()))  # type: ignore

        if route is not None:
            router.add_api_route(
                route.path,
                route.endpoint,
                methods=route.methods,
            )

    return router
