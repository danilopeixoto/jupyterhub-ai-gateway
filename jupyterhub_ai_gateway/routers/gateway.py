"""
Gateway router module.
"""

from fastapi import APIRouter, Security
from mlflow.deployments.server.app import (
    Limiter,
    _load_route_config,
    create_app_from_config,
)

from ..constants import gateway_routes
from ..security import get_current_user
from ..utils import get_rate_limit_key


def create_router(config_path: str) -> APIRouter:
    """
    Create gateway router.

    Paramaters:
        config_path (str): Path to configuration file.

    Returns:
        APIRouter: The router.
    """

    scopes = ["custom:ai-gateway:full-access"]

    router = APIRouter(
        dependencies=[Security(get_current_user, scopes=scopes)],
    )

    config = _load_route_config(config_path)
    limiter = Limiter(key_func=get_rate_limit_key)

    app = create_app_from_config(config)
    app.state.limiter = limiter
    app.set_dynamic_routes(config, limiter)

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
