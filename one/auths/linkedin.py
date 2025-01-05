"""Do not use the objects of this code. Improve and move to views!"""

from __future__ import annotations

import requests
from django.conf import settings

author_id = settings.LINKEDIN_AUTHOR_ID
access_token = settings.LINKEDIN_ACCESS_TOKEN
client_id = settings.LINKEDIN_CLIENT_ID
state = settings.LINKEDIN_STATE
redirect_uri = "http://192.168.0.10/social-media/linkedin/process-code"


def linkedin_authorize():
    """Authorizes the user and opens a browser window to get the code."""

    url = "https://www.linkedin.com/oauth/v2/authorization"
    payload = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": "r_liteprofile r_emailaddress w_member_social",
    }
    response = requests.Request("GET", url, params=payload)
    url = response.prepare().url
    return url


def get_linkedin_access_token(code):
    """Returns an access token."""

    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": settings.LINKEDIN_CLIENT_ID,
        "client_secret": settings.LINKEDIN_CLIENT_SECRET,
    }
    response = requests.post(url, params=payload)
    access_token = response.json()["access_token"]
    return access_token
