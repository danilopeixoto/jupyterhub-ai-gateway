"""
Service application module.
"""

import os

from fastapi import FastAPI

from . import __version__
from .routers import gateway, service


def create_app(config_path: str) -> FastAPI:
    """
    Create service application:

    Paramaters:
        config_path (str): Path to configuration file.

    Returns:
        FastAPI: The application.
    """

    prefix = os.environ["JUPYTERHUB_SERVICE_PREFIX"]

    app = FastAPI(
        title="JupyterHub AI Gateway",
        description="AI gateway service for JupyterHub.",
        version=__version__,
        openapi_url=f"{prefix}/openapi.json",
        docs_url=f"{prefix}/docs",
        redoc_url=f"{prefix}/redoc",
        swagger_ui_init_oauth={"clientId": os.environ["JUPYTERHUB_CLIENT_ID"]},
        swagger_ui_oauth2_redirect_url=os.environ["JUPYTERHUB_OAUTH_CALLBACK_URL"],
    )

    service_router = service.create_router()
    app.include_router(service_router, prefix=prefix)

    gateway_router = gateway.create_router(config_path)
    app.include_router(gateway_router, prefix=prefix)

    return app
