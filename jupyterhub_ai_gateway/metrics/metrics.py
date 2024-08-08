"""
Metric definitions module.
"""

from prometheus_client import Counter, Histogram, Summary

#: Total number of HTTP requests.
http_requests_total = Counter(
    name="http_requests_total",
    documentation="Total number of HTTP requests.",
    labelnames=["endpoint", "method", "status"],
)

#: HTTP request duration in seconds (latency).
http_request_duration = Histogram(
    name="http_request_duration",
    documentation="HTTP request duration in seconds (latency).",
    labelnames=["endpoint", "method"],
    unit="seconds",
    buckets=[
        0.01,
        0.025,
        0.05,
        0.075,
        0.1,
        0.25,
        0.5,
        0.75,
        1.0,
        2.5,
        5.0,
        7.5,
        10.0,
        20.0,
        30.0,
        40.0,
        50.0,
        60.0,
    ],
)

#: HTTP request size in bytes.
http_request_size = Summary(
    name="http_request_size",
    documentation="HTTP request size in bytes.",
    labelnames=["endpoint", "method"],
    unit="bytes",
)

#: HTTP response size in bytes.
http_response_size = Summary(
    name="http_response_size",
    documentation="HTTP response size in bytes.",
    labelnames=["endpoint", "method"],
    unit="bytes",
)
