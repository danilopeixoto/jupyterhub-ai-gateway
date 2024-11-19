"""
Gateway router module.
"""

from fastapi import APIRouter, Security
from mlflow.gateway.app import Limiter, _load_route_config, create_app_from_config

from ..constants import gateway_routes
from ..security import get_current_user
from ..utils import get_rate_limit_key, match_path


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

    for gateway_route in gateway_routes:
        for route in app.routes:
            matches_path = match_path(gateway_route["path"], route.path)  # type: ignore
            matches_methods = gateway_route["methods"] == tuple(route.methods)  # type: ignore

            if matches_path and matches_methods:
                router.add_api_route(
                    route.path,  # type: ignore
                    route.endpoint,  # type: ignore
                    methods=route.methods,  # type: ignore
                )

    return router
