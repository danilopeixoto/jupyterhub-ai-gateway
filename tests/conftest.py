"""
Test configuration module.
"""

# pylint: disable=redefined-outer-name

import os

import pytest
from fastapi import APIRouter
from fastapi.testclient import TestClient

from jupyterhub_ai_gateway.app import create_app
from jupyterhub_ai_gateway.routers.gateway import create_router


@pytest.fixture
def config_path() -> str:
    """
    Return configuration path.

    Returns:
        str: The configuration path.
    """

    path = os.path.join(os.path.dirname(__file__), "data", "test-config.yaml")
    return path


@pytest.fixture
def gateway_router(config_path: str) -> APIRouter:
    """
    Return gateway router.

    Parameters:
        config_path (str): The configuration path.

    Returns:
        APIRouter: The API router.
    """

    router = create_router(config_path)
    return router


@pytest.fixture
def client(config_path: str) -> TestClient:
    """
    Return test client.

    Parameters:
        config_path (str): The configuration path.

    Returns:
        TestClient: The test client.
    """

    app = create_app(config_path, enable_metrics=True)
    return TestClient(app)
