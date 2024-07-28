"""
Security module.
"""

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2AuthorizationCodeBearer, SecurityScopes
from fastapi.security.api_key import APIKeyQuery

from .client import get_client
from .models import User
from .settings import settings


async def get_current_user(
    security_scopes: SecurityScopes,
    request: Request,
    token_parameter: str = Depends(APIKeyQuery(name="token", auto_error=False)),
    authorization_header: str = Depends(
        OAuth2AuthorizationCodeBearer(
            authorizationUrl=settings.jupyterhub_public_hub_url
            + "/hub/api/oauth2/authorize",
            tokenUrl="get_token",
            auto_error=False,
        ),
    ),
) -> User:
    """
    Retrieve the current user based on the provided token parameter or authorization header.

    Args:
        security_scopes (SecurityScopes): Scopes required for accessing the resource.
        request (Request): The incoming request object.
        token_parameter (str): Token provided as a query parameter.
        authorization_header (str): Token provided in the authorization header.

    Returns:
        User: User object representing the authenticated user.

    Raises:
        HTTPException: If authentication fails due to missing or invalid token,
            or if user is not authorized based on access scopes.
    """

    token = token_parameter or authorization_header

    if token is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="User must provide token query parameter or authorization bearer header.",
        )

    async with get_client() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/user", headers=headers)

        if response.is_error:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail={
                    "msg": "Error getting user information from token.",
                    "request_url": str(response.request.url),
                    "token": token,
                    "response_code": response.status_code,
                    "hub_response": response.json(),
                },
            )

    user = User(**response.json())
    request.state.user_id = user.name

    if any(scope in user.scopes for scope in security_scopes.scopes):
        return user

    raise HTTPException(
        status.HTTP_403_FORBIDDEN,
        detail=(
            "User not authorized. "
            f"Required scopes include one of the following: {security_scopes.scopes}."
        ),
    )
