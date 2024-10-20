import ssl

import requests
from django.conf import settings
from huey.contrib import djhuey as huey


class Bot:
    ssl._create_default_https_context = ssl._create_unverified_context
    base_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_API_KEY}/"

    @huey.task()
    def to_chat(chat_id: str, text: str, file_url=None):
        """Send text message to a chat"""

        if file_url is None:
            params = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
            requests.get(Bot.base_url + "sendMessage", params=params)
        else:
            cparams = {"chat_id": chat_id, "caption": text}
            if requests.get(Bot.base_url + "sendPhoto", params=cparams | {"photo": file_url}).status_code != 200:
                requests.get(Bot.base_url + "sendDocument", params=cparams | {"document": file_url})

    def to_admin(text: str):
        """Send text message to the admin"""
        processed_text = f"{settings.WEBSITE_NAME} - {settings.WEBSITE_URL}:\n\n{text}"
        Bot.to_chat(chat_id=settings.TELEGRAM_ADMIN_CHAT_ID, text=processed_text)

    def to_group(cls, group_id, text, file_url=None):
        """Send text and optionally an image to a group"""
        chat_id = "@" + group_id if not group_id.startswith("@") else group_id
        Bot.to_chat(chat_id, text, file_url)
