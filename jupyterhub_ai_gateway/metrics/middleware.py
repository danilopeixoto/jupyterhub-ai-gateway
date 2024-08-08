"""
Metrics middleware module.
"""

import logging
from timeit import default_timer
from typing import Callable, List, Optional

from fastapi import Request, Response

from .metrics import (
    http_request_duration,
    http_request_size,
    http_requests_total,
    http_response_size,
)

logger = logging.getLogger(__name__)


def make_metrics_middleware(exclude_paths: Optional[List[str]] = None) -> Callable:
    """
    Create metrics middleware.

    Parameters:
        exclude_paths (Optional[List[str]]): List of endpoint paths to exclude. Defaults to none.

    Returns:
        Callable: The middleware.
    """

    if exclude_paths is None:
        exclude_paths = []

    async def metrics_middleware(request: Request, call_next: Callable) -> Response:
        """
        Middleware to capture metrics for HTTP requests and responses.

        Measures request count, duration (latency), request size, and response size.

        Parameters:
            request (Request): The incoming HTTP request.
            call_next (Callable): Function to process the request and return a response.

        Returns:
            Response: The HTTP response.
        """

        if any(request.url.path.startswith(path) for path in exclude_paths):
            return await call_next(request)

        start_time = default_timer()
        response = await call_next(request)
        request_duration = max(default_timer() - start_time, 0)

        try:
            endpoint = request.url.path
            method = request.method
            status = str(response.status_code)

            request_size = int(request.headers.get("Content-Length", 0))
            response_size = int(response.headers.get("Content-Length", 0))

            http_requests_total.labels(
                endpoint=endpoint,
                method=method,
                status=status,
            ).inc()

            http_request_duration.labels(
                endpoint=endpoint,
                method=method,
            ).observe(request_duration)

            http_request_size.labels(
                endpoint=endpoint,
                method=method,
            ).observe(request_size)

            http_response_size.labels(
                endpoint=endpoint,
                method=method,
            ).observe(response_size)
        except Exception:  # pylint: disable=broad-exception-caught
            logger.exception("Could not log metrics.")

        return response

    return metrics_middleware
