"""
Hub client module.
"""

import httpx

from .settings import settings


def get_client() -> httpx.AsyncClient:
    """
    Get hub client.

    Returns:
        httpx.AsyncClient: Asynchronous HTTP client.
    """

    base_url = settings.jupyterhub_api_url
    token = settings.jupyterhub_api_token

    headers = {"Authorization": f"Bearer {token}"}

    return httpx.AsyncClient(base_url=base_url, headers=headers)
