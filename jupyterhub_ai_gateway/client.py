"""
Hub client module.
"""

import os

import httpx


def get_client() -> httpx.AsyncClient:
    """
    Get hub client.

    Returns:
        httpx.AsyncClient: Asynchronous HTTP client.
    """

    base_url = os.environ["JUPYTERHUB_API_URL"]
    token = os.environ["JUPYTERHUB_API_TOKEN"]
    headers = {"Authorization": f"Bearer {token}"}

    return httpx.AsyncClient(base_url=base_url, headers=headers)
