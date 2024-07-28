"""
Service constants.
"""

#: Gateway routes to export.
gateway_routes = [
    {"path": "/api/2.0/endpoints/{endpoint_name}", "methods": ("GET",)},
    {"path": "/api/2.0/endpoints/", "methods": ("GET",)},
    {"path": "/endpoints/completions/invocations", "methods": ("POST",)},
    {"path": "/endpoints/chat/invocations", "methods": ("POST",)},
    {"path": "/endpoints/embeddings/invocations", "methods": ("POST",)},
    {"path": "/v1/completions", "methods": ("POST",)},
    {"path": "/v1/chat/completions", "methods": ("POST",)},
    {"path": "/v1/embeddings", "methods": ("POST",)},
]
