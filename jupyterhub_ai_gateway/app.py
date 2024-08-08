"""
Service application module.
"""

from fastapi import FastAPI

from . import __version__
from .metrics.middleware import make_metrics_middleware
from .routers import gateway, service
from .settings import settings


def create_app(config_path: str, enable_metrics: bool = False) -> FastAPI:
    """
    Create service application:

    Paramaters:
        config_path (str): Path to configuration file.
        enable_metrics (bool): Enable server metrics. Defaults to false.

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

    service_router = service.create_router(enable_metrics)
    app.include_router(service_router, prefix=prefix)

    gateway_router = gateway.create_router(config_path)
    app.include_router(gateway_router, prefix=prefix)

    if enable_metrics:
        metrics_middleware = make_metrics_middleware(
            exclude_paths=["/health", "/metrics", "/openapi.json"]
        )

        app.middleware("http")(metrics_middleware)

    return app
