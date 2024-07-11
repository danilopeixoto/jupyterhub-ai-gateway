"""
Service constants.
"""

#: Gateway routes to export.
gateway_routes = [
    {"path": "/api/2.0/endpoints/{endpoint_name}", "methods": ("GET",)},
    {"path": "/api/2.0/endpoints/", "methods": ("GET",)},
    {"path": "/api/2.0/endpoints/limits/{endpoint}", "methods": ("GET",)},
    {"path": "/api/2.0/gateway/routes/{route_name}", "methods": ("GET",)},
    {"path": "/api/2.0/gateway/routes/", "methods": ("GET",)},
    {"path": "/api/2.0/gateway/limits/{endpoint}", "methods": ("GET",)},
    {"path": "/endpoints/completions/invocations", "methods": ("POST",)},
    {"path": "/endpoints/chat/invocations", "methods": ("POST",)},
    {"path": "/endpoints/embeddings/invocations", "methods": ("POST",)},
    {"path": "/gateway/completions/invocations", "methods": ("POST",)},
    {"path": "/gateway/chat/invocations", "methods": ("POST",)},
    {"path": "/gateway/embeddings/invocations", "methods": ("POST",)},
    {"path": "/v1/completions", "methods": ("POST",)},
    {"path": "/v1/chat/completions", "methods": ("POST",)},
    {"path": "/v1/embeddings", "methods": ("POST",)},
]
