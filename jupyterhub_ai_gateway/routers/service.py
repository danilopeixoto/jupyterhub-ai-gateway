"""
Service router module.
"""

import os

from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse

from .. import __version__
from ..client import get_client
from ..models import HealthStatus


def create_router() -> APIRouter:
    """
    Create service router.

    Returns:
        APIRouter: The router.
    """

    router = APIRouter()

    @router.get("/")
    async def get_status() -> HealthStatus:
        """
        Get service health status.

        Returns:
            HealthStatus: The service health status response.
        """

        return HealthStatus(version=__version__)

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
            os.environ["JUPYTERHUB_PUBLIC_URL"]
            + os.environ["JUPYTERHUB_OAUTH_CALLBACK_URL"]
        )

        async with get_client() as client:
            data = {
                "client_id": os.environ["JUPYTERHUB_CLIENT_ID"],
                "client_secret": os.environ["JUPYTERHUB_API_TOKEN"],
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
            }

            response = await client.post("/oauth2/token", data=data)

        return response.json()

    return router
