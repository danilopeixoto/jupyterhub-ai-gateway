"""
Utility test module.
"""

import pytest

from jupyterhub_ai_gateway.utils import match_path


@pytest.mark.parametrize(
    "path, pattern, expected",
    [
        (
            "/api/2.0/endpoints/{endpoint_name}",
            "/api/2.0/endpoints/{endpoint_name}",
            True,
        ),
        ("/api/2.0/endpoints/", "/api/2.0/endpoints/", True),
        ("/api/2.0/gateway/routes/", "/api/2.0/gateway/routes/", True),
        ("/endpoints/*/call", "/endpoints/chat/invocations", False),
        (
            "/api/2.0/gateway/routes/{name}",
            "/api/2.0/gateway/routes/{route_name}",
            False,
        ),
    ],
)
def test_match_path(pattern: str, path: str, expected: bool):
    """
    Test if path matches pattern.

    Parameters:
        pattern (str): The pattern to match against.
        path (str): The path to be tested.
        expected (bool): The expected result of the match.

    Raises:
        AssertionError: If the match result does not match the expected value.
    """

    assert match_path(pattern, path) == expected
