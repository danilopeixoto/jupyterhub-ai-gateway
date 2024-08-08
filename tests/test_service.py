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


def test_get_metrics(client: TestClient):
    """
    Test the metrics endpoint.

    Parameters:
        client (TestClient): The gateway test client.

    Raises:
        AssertionError: If the response does not match the expected format.
    """

    expected_metrics = [
        "http_requests_total",
        "http_request_duration_seconds",
        "http_request_size_bytes",
        "http_response_size_bytes",
    ]

    response = client.get(f"{settings.jupyterhub_service_prefix}/metrics")
    assert response.status_code == 200

    data = response.text

    for metric in expected_metrics:
        assert metric in data
