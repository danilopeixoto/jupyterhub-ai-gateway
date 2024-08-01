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


def match_path(pattern: str, path: str) -> bool:
    """
    Check if the given path matches the specified pattern.

    The pattern can contain wildcards (`*`) that match any single path segment.

    Parameters:
        pattern (str): The pattern to match against.
        path (str): The path to be matched.

    Returns:
        bool: `True` if the path matches the pattern, `False` otherwise.
    """

    pattern_parts = pattern.strip("/").split("/")
    path_parts = path.strip("/").split("/")

    if len(pattern_parts) != len(path_parts):
        return False

    for pattern_part, path_part in zip(pattern_parts, path_parts):
        if pattern_part == "*":
            continue

        if pattern_part != path_part:
            return False

    return True
