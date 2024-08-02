"""
Service router test module.
"""

from fastapi.testclient import TestClient

import jupyterhub_ai_gateway
from jupyterhub_ai_gateway.settings import settings


def test_get_status(client: TestClient):
    """
    Test the health status endpoint.

    Parameters:
        client (TestClient): The gateway test client.

    Raises:
        AssertionError: If the response does not match the expected format.
    """

    response = client.get(f"{settings.jupyterhub_service_prefix}/health")
    assert response.status_code == 200

    data = response.json()

    assert "status" in data
    assert data["status"] == "OK"

    assert "version" in data
    assert data["version"] == jupyterhub_ai_gateway.__version__
