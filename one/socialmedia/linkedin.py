import json
import re
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.urls import reverse

LINKEDIN_API_URL = "https://api.linkedin.com/rest"
DEFAULT_VERSION = "202507"

# Linkedin App
# LINKEDIN_APP = {'client_id': '', 'secret': '', 'key': ''}
LINKEDIN_APP = settings.SOCIALACCOUNT_PROVIDERS["linkedin_oauth2"]["APP"]
APP_CLIENT_ID = LINKEDIN_APP["client_id"]
APP_SECRET = LINKEDIN_APP["secret"]


class FileInputNotSupported(Exception):
    pass


def escape_little_text(text: str) -> str:
    return re.sub(r"([,{}@[\]()<>#*_~,])", r"\\\1", text)


class LinkedinClient:
    def __init__(
        self,
        access_token: str,
        author_type: str,
        author_id: str | int,
        version: str = DEFAULT_VERSION,
    ):
        self.access_token = access_token
        self.author_type = author_type
        self.author_id = author_id
        self.version = version

    @staticmethod
    def get_authorization_url(scopes: list[str] | None = None) -> str:
        """Generate the LinkedIn authorization URL to obtain an authorization code."""
        # https://learn.microsoft.com/en-us/linkedin/shared/authentication/authorization-code-flow?tabs=HTTPS1#step-2-request-an-authorization-code
        if scopes is None:
            scopes = [
                "r_liteprofile",
                "r_emailaddress",
                "w_member_social",
                "r_member_social",
                "w_organization_social",
                "r_organization_social",
            ]

        base_url = "https://www.linkedin.com/oauth/v2/authorization"
        query_params = {
            "response_type": "code",
            "client_id": APP_CLIENT_ID,
            "redirect_uri": settings.MAIN_WEBSITE_URL + reverse("linkedin_callback"),
            "scope": " ".join(scopes),
        }
        return f"{base_url}?{urlencode(query_params)}"

    @staticmethod
    def regenerate_access_token(
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        authorization_code: str,
    ) -> str:
        """Request a new access token using an authorization code."""
        url = "https://www.linkedin.com/oauth/v2/accessToken"
        payload = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()["access_token"]

    def _build_headers(self, extra: dict | None = None) -> dict:
        base = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": self.version,
        }
        return base | (extra or {})

    def _author_urn(self) -> str:
        return f"urn:li:{self.author_type}:{self.author_id}"

    def comment_on_post(self, post_urn: str, text: str, content=None):
        url = (
            f"{LINKEDIN_API_URL}/socialActions/{urllib.parse.quote(post_urn)}/comments"
        )
        payload = {
            "actor": self._author_urn(),
            "object": post_urn,
            "message": {"text": text},
        }
        if content:
            payload["content"] = content
        return requests.post(
            url, headers=self._build_headers(), data=json.dumps(payload).encode("utf-8")
        )

    def _init_image_upload(self):
        url = f"{LINKEDIN_API_URL}/images?action=initializeUpload"
        payload = {"initializeUploadRequest": {"owner": self._author_urn()}}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers=self._build_headers(), method="POST"
        )
        with urllib.request.urlopen(req) as res:
            value = json.loads(res.read().decode("utf-8"))["value"]
        return value["uploadUrl"], value["image"]

    def upload_image(self, file: bytes | str | Path):
        if isinstance(file, bytes):
            file_bytes = file
        elif isinstance(file, str | Path):
            with open(file, "rb") as f:
                file_bytes = f.read()
        else:
            raise FileInputNotSupported("Invalid file input type.")

        upload_url, image_urn = self._init_image_upload()
        headers = {"Authorization": f"Bearer {self.access_token}"}
        res = requests.put(upload_url, headers=headers, data=file_bytes)
        return res, image_urn

    def get_image(self, image_urn: str):
        url = f"{LINKEDIN_API_URL}/images/{urllib.parse.quote(image_urn)}"
        req = urllib.request.Request(url, headers=self._build_headers())
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
        return res, data

    def share_post(
        self,
        comment: str,
        visibility: str = "PUBLIC",
        feed_distribution: str = "MAIN_FEED",
        reshable_disabled: bool = False,
        content=None,
        container=None,
    ):
        url = f"{LINKEDIN_API_URL}/posts"
        payload = {
            "author": self._author_urn(),
            "commentary": comment,
            "visibility": visibility,
            "distribution": {
                "feedDistribution": feed_distribution,
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": reshable_disabled,
        }
        if content:
            payload["content"] = content
        if container:
            payload["container"] = container

        return requests.post(
            url, headers=self._build_headers(), data=json.dumps(payload).encode("utf-8")
        )

    def share_poll(
        self,
        comment: str,
        question: str,
        options: list[str],
        duration: str = "THREE_DAYS",
        visibility: str = "PUBLIC",
        feed_distribution: str = "MAIN_FEED",
        reshable_disabled: bool = False,
        container: str | None = None,
    ):
        content = {
            "poll": {
                "question": question,
                "options": [{"text": option} for option in options],
                "settings": {"duration": duration},
            }
        }
        return self.share_post(
            comment=comment,
            visibility=visibility,
            feed_distribution=feed_distribution,
            reshable_disabled=reshable_disabled,
            content=content,
            container=container,
        )

    def share_post_with_media(
        self,
        comment: str,
        media_id: str,
        media_title: str | None = None,
        visibility: str = "PUBLIC",
        feed_distribution: str = "MAIN_FEED",
        reshable_disabled: bool = False,
        container: str | None = None,
    ):
        content = {"media": {"id": media_id}}
        if media_title:
            content["media"]["title"] = media_title
        return self.share_post(
            comment=comment,
            visibility=visibility,
            feed_distribution=feed_distribution,
            reshable_disabled=reshable_disabled,
            content=content,
            container=container,
        )

    def delete_post(self, urn: str):
        url = f"{LINKEDIN_API_URL}/posts/{urllib.parse.quote(urn)}"
        headers = self._build_headers(extra={"X-RestLi-Method": "DELETE"})
        return requests.delete(url, headers=headers)
