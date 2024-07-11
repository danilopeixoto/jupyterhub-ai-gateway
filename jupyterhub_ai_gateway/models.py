"""
Service models.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class HealthStatus(BaseModel):
    """
    Health status response.
    """

    status: str
    version: str


class Server(BaseModel):
    """
    Server information response.
    """

    name: str
    ready: bool
    stopped: Optional[bool] = None
    pending: Optional[str] = None
    url: str
    progress_url: str
    full_url: Optional[str] = None
    full_progress_url: Optional[str] = None
    started: datetime
    last_activity: datetime
    state: Optional[Any] = None
    user_options: Optional[Any] = None


class User(BaseModel):
    """
    User response.
    """

    name: str
    admin: bool
    roles: Optional[List[str]] = None
    groups: Optional[List[str]] = None
    server: Optional[str] = None
    pending: Optional[str] = None
    last_activity: Optional[datetime] = None
    servers: Optional[Dict[str, Server]] = None
    auth_state: Optional[Any] = None
    session_id: Optional[str] = None
    scopes: List[str]
    token_id: Optional[str] = None


class AuthorizationError(BaseModel):
    """
    Authorization error response.
    """

    detail: str


class ForbiddenError(BaseModel):
    """
    Forbidden error response.
    """

    detail: str


class HubApiErrorDetail(BaseModel):
    """
    Hub API error detail.
    """

    msg: str
    request_url: str
    token: str
    response_code: int
    hub_response: Any


class HubApiError(BaseModel):
    """
    Hub API error response.
    """

    detail: HubApiErrorDetail
