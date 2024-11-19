"""
Gateway router test module.
"""

from typing import Any
from unittest.mock import AsyncMock, patch

import httpx
from fastapi import APIRouter
from fastapi.testclient import TestClient
from mlflow.gateway.schemas import chat, completions

from jupyterhub_ai_gateway.settings import settings


def test_gateway_router(gateway_router: APIRouter):
    """
    Test to ensure all gateway routes are in the router.

    Parameters:
        gateway_router (APIRouter): The gateway router.

    Raises:
        AssertionError: If there are gateway routes that are not found in the router.
    """

    expected_routes = [
        {"path": "/api/2.0/endpoints/{endpoint_name}", "methods": ("GET",)},
        {"path": "/api/2.0/endpoints/", "methods": ("GET",)},
        {"path": "/api/2.0/gateway/routes/{route_name}", "methods": ("GET",)},
        {"path": "/api/2.0/gateway/routes/", "methods": ("GET",)},
        {"path": "/endpoints/completions/invocations", "methods": ("POST",)},
        {"path": "/endpoints/chat/invocations", "methods": ("POST",)},
        {"path": "/endpoints/embeddings/invocations", "methods": ("POST",)},
        {"path": "/endpoints/completions/invocations", "methods": ("POST",)},
        {"path": "/endpoints/chat/invocations", "methods": ("POST",)},
        {"path": "/endpoints/embeddings/invocations", "methods": ("POST",)},
        {"path": "/gateway/completions/invocations", "methods": ("POST",)},
        {"path": "/gateway/chat/invocations", "methods": ("POST",)},
        {"path": "/gateway/embeddings/invocations", "methods": ("POST",)},
        {"path": "/gateway/completions/invocations", "methods": ("POST",)},
        {"path": "/gateway/chat/invocations", "methods": ("POST",)},
        {"path": "/gateway/embeddings/invocations", "methods": ("POST",)},
        {"path": "/v1/completions", "methods": ("POST",)},
        {"path": "/v1/chat/completions", "methods": ("POST",)},
        {"path": "/v1/embeddings", "methods": ("POST",)},
    ]

    routes = [
        {"path": route.path, "methods": tuple(route.methods)}  # type: ignore
        for route in gateway_router.routes
    ]

    assert routes == expected_routes


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


@patch("mlflow.gateway.app.get_provider")
@patch(
    "jupyterhub_ai_gateway.client.httpx.AsyncClient.get",
    return_value=httpx.Response(
        200,
        request=httpx.Request("GET", "url"),
        json={
            "name": "user",
            "admin": False,
            "scopes": ["custom:ai-gateway:full-access"],
        },
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

    json_data = response.json()

    assert "model" in json_data
    assert json_data["model"] == "completions"


@patch("mlflow.gateway.app.get_provider")
@patch(
    "jupyterhub_ai_gateway.client.httpx.AsyncClient.get",
    return_value=httpx.Response(
        200,
        request=httpx.Request("GET", "url"),
        json={
            "name": "user",
            "admin": False,
            "scopes": ["custom:ai-gateway:full-access"],
        },
    ),
)
def test_openai_rate_limit(
    get_mock: Any,  # pylint: disable=unused-argument
    get_provider_mock: Any,
    client: TestClient,
):
    """
    Test OpenAI endpoint with rate limit.

    Parameters:
        get_mock (Any): Mock object.
        get_provider (Any): Mock object.
        client (TestClient): The gateway router test client.

    Raises:
        AssertionError: If rate limit is not applied.
    """

    provider_mock = AsyncMock()
    provider_mock.chat.return_value = chat.ResponsePayload(
        model="chat",
        created=0,
        choices=[],
        usage=chat.ChatUsage(),
    )
    get_provider_mock.return_value = lambda route: provider_mock

    headers = {
        "Authorization": "Bearer <valid-token>",
    }

    data = {
        "model": "chat",
        "messages": [
            {
                "role": "user",
                "content": "The quick brown fox...",
            },
        ],
        "max_tokens": 64,
    }

    limit = 2

    for i in range(limit + 1):
        response = client.post(
            f"{settings.jupyterhub_service_prefix}/v1/chat/completions",
            headers=headers,
            json=data,
        )

        if i < limit:
            assert response.status_code == 200

            json_data = response.json()

            assert "model" in json_data
            assert json_data["model"] == "chat"
        else:
            assert response.status_code == 200  # TODO(429)
