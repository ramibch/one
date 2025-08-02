import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

import requests

from one.bot import Bot

DEFAULT_VERSION = "202507"
LINKEDIN_API_URL = "https://api.linkedin.com/rest"


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

    def build_headers(self, extra: dict | None = None) -> dict:
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

        data = json.dumps(payload).encode("utf-8")
        return requests.post(url, headers=self.build_headers(), json=data)

    def get_me(self):
        url = "https://api.linkedin.com/v2/me"
        return requests.get(url, headers=self.build_headers())

    def _init_image_upload(self):
        url = f"{LINKEDIN_API_URL}/images?action=initializeUpload"
        payload = {"initializeUploadRequest": {"owner": self._author_urn()}}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, json=data, headers=self.build_headers(), method="POST"
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
        res = requests.put(upload_url, headers=headers, json=file_bytes)
        return res, image_urn

    def get_image(self, image_urn: str):
        url = f"{LINKEDIN_API_URL}/images/{urllib.parse.quote(image_urn)}"
        req = urllib.request.Request(url, headers=self.build_headers())
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

        response = requests.post(
            url,
            headers=self.build_headers(),
            json=json.dumps(payload).encode("utf-8"),
        )
        if response.status_code > 300:
            msg = f"Failed to post to Linkedin:\n\n{response.text}\n\n{response.json()}"
            Bot.to_admin(msg)

        return response

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
        headers = self.build_headers(extra={"X-RestLi-Method": "DELETE"})
        return requests.delete(url, headers=headers)
