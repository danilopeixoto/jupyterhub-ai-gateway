"""
Service router module.
"""

from fastapi import APIRouter, Form
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import HTMLResponse, JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from .. import __version__
from ..client import get_client
from ..models import HealthStatus
from ..settings import settings


def create_router(enable_metrics: bool) -> APIRouter:
    """
    Create service router.

    Parameters:
        enable_metrics (bool): Enable server metrics.

    Returns:
        APIRouter: The router.
    """

    router = APIRouter()

    @router.get("/", include_in_schema=False)
    async def get_docs() -> HTMLResponse:
        """
        Get service documentation.

        Returns:
            HTMLResponse: The documentation HTML response.
        """

        return get_swagger_ui_html(
            openapi_url="openapi.json",
            title=settings.jupyterhub_ai_gateway_docs_title,
            init_oauth={"clientId": settings.jupyterhub_client_id},
            oauth2_redirect_url=settings.jupyterhub_oauth_callback_url,
        )

    @router.get(settings.jupyterhub_oauth_callback_url, include_in_schema=False)
    async def oauth_callback() -> HTMLResponse:
        """
        Handles the OAuth callback.

        Returns:
            HTMLResponse: The OAuth redirect HTML response.
        """

        return get_swagger_ui_oauth2_redirect_html()

    @router.get("/health")
    async def get_status() -> HealthStatus:
        """
        Get service health status.

        Returns:
            HealthStatus: The service health status response.
        """

        return HealthStatus(status="OK", version=__version__)

    @router.get("/metrics", include_in_schema=False)
    async def get_metrics() -> Response:
        """
        Get server metrics.

        Returns:
            Response: The server metrics response if metrics are enabled.
                      Otherwise, returns a NotFound (404) response.
        """

        if enable_metrics:
            return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

        return Response(content="Metrics are not enabled.", status_code=404)

    @router.post("/get_token", include_in_schema=False)
    async def get_token(code: str = Form(...)) -> JSONResponse:
        """
        Get token callback for OAuth2 scheme.

        This endpoint retrieves an OAuth2 token using the provided authorization code.

        Args:
            code (str): Authorization code obtained from the OAuth2 authorization flow.

        Returns:
            JSONResponse: The OAuth2 token endpoint response.
        """

        redirect_uri = (
            settings.jupyterhub_public_url + settings.jupyterhub_oauth_callback_url
        )

        async with get_client() as client:
            data = {
                "client_id": settings.jupyterhub_client_id,
                "client_secret": settings.jupyterhub_api_token,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            }

            response = await client.post("/oauth2/token", data=data)

        return response.json()

    return router
