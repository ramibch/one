from urllib.parse import urlencode

import requests
from django.conf import settings
from django.urls import reverse_lazy

from one.bot import Bot


def get_linkedin_redirect_uri():
    return settings.MAIN_WEBSITE_URL + reverse_lazy("linkedin_callback")


def get_linkedin_access_from_code(code: str) -> dict:
    """
    Request an access token using an authorization code.
    """

    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_SECRET_KEY,
        "redirect_uri": get_linkedin_redirect_uri(),
    }

    response = requests.post(url, data=payload)
    if response.status_code >= 400:
        Bot.to_admin(f"Error generating linkedin access:\b\n{response.text}")
    response.raise_for_status()
    return response.json()


def refresh_linkedin_access(refresh_token: str) -> dict:
    """
    Get a new access token using a refresh token.

    https://learn.microsoft.com/en-us/linkedin/shared/authentication/programmatic-refresh-tokens

    """

    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_SECRET_KEY,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code >= 400:
        Bot.to_admin(f"Error generating linkedin access:\b\n{response.text}")
    response.raise_for_status()
    return response.json()


def get_linkedin_auth_url(state, scopes: list[str] | None = None) -> str:
    """
    Generate the LinkedIn authorization URL to obtain an authorization code.
    """
    # https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?tabs=HTTPS1#step-2-request-an-authorization-code
    if scopes is None:
        scopes = [
            "r_liteprofile",
            "r_emailaddress",
            "w_member_social",
            "w_organization_social",
            "r_organization_social",
        ]

    base_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "redirect_uri": get_linkedin_redirect_uri(),
        "state": state,
        "scope": " ".join(scopes),
    }
    return f"{base_url}?{urlencode(params)}"
