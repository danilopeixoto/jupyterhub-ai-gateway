"""
Settings module.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings model.
    """

    jupyterhub_ai_gateway_config: str = "config.yaml"
    jupyterhub_service_name: str = "ai-gateway"
    jupyterhub_service_prefix: str = ""
    jupyterhub_api_url: str = "http://localhost:8000/hub/api"
    jupyterhub_api_token: str = "<service-api-token>"
    jupyterhub_client_id: str = "service-ai-gateway"
    jupyterhub_oauth_callback_url: str = "/oauth_callback"
    jupyterhub_public_url: str = "http://localhost:5000"
    jupyterhub_public_hub_url: str = "http://localhost:8000"


#: Settings instance.
settings = Settings()
