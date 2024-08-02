"""
Service application module.
"""

from fastapi import FastAPI

from . import __version__
from .routers import gateway, service
from .settings import settings


def create_app(config_path: str) -> FastAPI:
    """
    Create service application:

    Paramaters:
        config_path (str): Path to configuration file.

    Returns:
        FastAPI: The application.
    """

    prefix = settings.jupyterhub_service_prefix

    app = FastAPI(
        title=settings.jupyterhub_ai_gateway_docs_title,
        description=settings.jupyterhub_ai_gateway_docs_description,
        version=__version__,
        openapi_url=f"{prefix}/openapi.json",
        swagger_ui_init_oauth={"clientId": settings.jupyterhub_client_id},
        swagger_ui_oauth2_redirect_url=settings.jupyterhub_oauth_callback_url,
        docs_url=None,
        redoc_url=None,
    )

    service_router = service.create_router()
    app.include_router(service_router, prefix=prefix)

    gateway_router = gateway.create_router(config_path)
    app.include_router(gateway_router, prefix=prefix)

    return app
