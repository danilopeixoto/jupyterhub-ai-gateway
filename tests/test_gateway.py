"""
Gateway router test module.
"""

from typing import Any
from unittest.mock import AsyncMock, patch

import httpx
from fastapi import APIRouter
from fastapi.testclient import TestClient
from mlflow.gateway.schemas import completions

from jupyterhub_ai_gateway.constants import gateway_routes
from jupyterhub_ai_gateway.settings import settings


def test_gateway_router(gateway_router: APIRouter):
    """
    Test to ensure all gateway routes are in the router.

    Parameters:
        gateway_router (APIRouter): The gateway router.

    Raises:
        AssertionError: If there are gateway routes that are not found in the router.
    """

    expected_routes = set(tuple(route.items()) for route in gateway_routes)

    routes = set(
        (("path", route.path), ("methods", tuple(route.methods)))  # type: ignore
        for route in gateway_router.routes
    )

    missing_routes = expected_routes - routes

    assert len(missing_routes) == 0


def test_openai_completions_without_access_token(client: TestClient):
    """
    Test OpenAI completions endpoint without access token.

    Parameters:
        client (TestClient): The gateway router test client.

    Raises:
        AssertionError: If the response is not unauthorized.
    """

    data = {
        "model": "completions",
        "prompt": "The quick brown fox...",
        "max_tokens": 64,
    }

    response = client.post(
        f"{settings.jupyterhub_service_prefix}/v1/completions", json=data
    )

    assert response.status_code == 401


@patch(
    "jupyterhub_ai_gateway.client.httpx.AsyncClient.get",
    return_value=httpx.Response(400, request=httpx.Request("GET", "url"), json={}),
)
def test_openai_completions_with_invalid_access_token(
    get_mock: Any, client: TestClient  # pylint: disable=unused-argument
):
    """
    Test OpenAI completions endpoint with invalid access token.

    Parameters:
        get_mock (Any): Mock object.
        client (TestClient): The gateway router test client.

    Raises:
        AssertionError: If the response is not unauthorized.
    """

    headers = {
        "Authorization": "Bearer <invalid-token>",
    }

    data = {
        "model": "completions",
        "prompt": "The quick brown fox...",
        "max_tokens": 64,
    }

    response = client.post(
        f"{settings.jupyterhub_service_prefix}/v1/completions",
        headers=headers,
        json=data,
    )

    assert response.status_code == 400


@patch("mlflow.deployments.server.app.get_provider")
@patch(
    "jupyterhub_ai_gateway.client.httpx.AsyncClient.get",
    return_value=httpx.Response(
        200,
        request=httpx.Request("GET", "url"),
        json={"name": "user", "admin": False, "scopes": ["access:services"]},
    ),
)
def test_openai_completions_with_valid_access_token(
    get_mock: Any,  # pylint: disable=unused-argument
    get_provider_mock: Any,
    client: TestClient,
):
    """
    Test OpenAI completions endpoint with valid access token.

    Parameters:
        get_mock (Any): Mock object.
        get_provider (Any): Mock object.
        client (TestClient): The gateway router test client.

    Raises:
        AssertionError: If the response is not successful.
    """

    provider_mock = AsyncMock()
    provider_mock.completions.return_value = completions.ResponsePayload(
        model="completions",
        created=0,
        choices=[],
        usage=completions.CompletionsUsage(),
    )
    get_provider_mock.return_value = lambda route: provider_mock

    headers = {
        "Authorization": "Bearer <valid-token>",
    }

    data = {
        "model": "completions",
        "prompt": "The quick brown fox...",
        "max_tokens": 64,
    }

    response = client.post(
        f"{settings.jupyterhub_service_prefix}/v1/completions",
        headers=headers,
        json=data,
    )

    assert response.status_code == 200

    data = response.json()

    assert "model" in data
    assert data["model"] == "completions"
