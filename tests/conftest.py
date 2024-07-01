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
