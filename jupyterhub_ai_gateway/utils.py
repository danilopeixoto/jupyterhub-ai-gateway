"""
Utility module.
"""

from fastapi import Request


def get_rate_limit_key(request: Request) -> str:
    """
    Retrieve the rate limit key from request.

    Use the `user_id` request state from authentication flow as rate limit key.

    Parameters:
        request (Request): The incoming request object.

    Returns:
        str: The rate limit key.
    """

    return request.state.user_id
