"""
Test configuration module.
"""

import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def environment():
    """
    Set environment variables.
    """

    os.environ["OPENAI_API_KEY"] = "<openai-api-key>"
    os.environ["JUPYTERHUB_SERVICE_NAME"] = "ai-gateway"
    os.environ["JUPYTERHUB_SERVICE_PREFIX"] = "/services/ai-gateway"
    os.environ["JUPYTERHUB_API_URL"] = "http://localhost:8000/hub/api"
    os.environ["JUPYTERHUB_API_TOKEN"] = "<service-api-token>"
    os.environ["JUPYTERHUB_CLIENT_ID"] = "service-ai-gateway"
    os.environ["JUPYTERHUB_OAUTH_CALLBACK_URL"] = "/services/ai-gateway/oauth_callback"
    os.environ["JUPYTERHUB_PUBLIC_URL"] = "http://localhost:5000"
    os.environ["JUPYTERHUB_PUBLIC_HUB_URL"] = "http://localhost:8000"
