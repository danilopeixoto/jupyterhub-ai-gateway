"""
Service router test module.
"""

from fastapi.testclient import TestClient

import jupyterhub_ai_gateway
from jupyterhub_ai_gateway.routers.service import create_router


def test_get_status():
    """
    Test the health status endpoint.

    Raises:
        AssertionError: If the response does not match the expected format.
    """

    router = create_router()
    client = TestClient(router)

    response = client.get("/")
    assert response.status_code == 200

    data = response.json()

    assert "version" in data
    assert data["version"] == jupyterhub_ai_gateway.__version__
