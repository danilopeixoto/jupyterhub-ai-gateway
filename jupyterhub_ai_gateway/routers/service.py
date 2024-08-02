"""
Service router module.
"""

from fastapi import APIRouter, Form
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse

from .. import __version__
from ..client import get_client
from ..models import HealthStatus
from ..settings import settings


def create_router() -> APIRouter:
    """
    Create service router.

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

    @router.get("/health")
    async def get_status() -> HealthStatus:
        """
        Get service health status.

        Returns:
            HealthStatus: The service health status response.
        """

        return HealthStatus(status="OK", version=__version__)

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
