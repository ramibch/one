import ssl

import requests
from django.conf import settings
from huey.contrib import djhuey as huey


class Bot:
    base_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_API_KEY}/"

    @staticmethod
    def prepare():
        ssl._create_default_https_context = ssl._create_unverified_context

    @staticmethod
    @huey.task()
    def to_chat(chat_id: str, text: str, file_url=None):
        """Send text message to a chat"""

        Bot.prepare()

        if file_url is None:
            params = {
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": True,
            }
            requests.get(Bot.base_url + "sendMessage", params=params)
        else:
            cparams = {"chat_id": chat_id, "caption": text}
            if (
                requests.get(
                    Bot.base_url + "sendPhoto", params=cparams | {"photo": file_url}
                ).status_code
                != 200
            ):
                requests.get(
                    Bot.base_url + "sendDocument",
                    params=cparams | {"document": file_url},
                )

    @staticmethod
    def to_admin(text: str):
        """Send text message to the admin"""
        Bot.to_chat(chat_id=settings.TELEGRAM_ADMIN_CHAT_ID, text=text)

    @staticmethod
    def to_group(group_id, text, file_url=None):
        """Send text and optionally an image to a group"""
        chat_id = "@" + group_id if not group_id.startswith("@") else group_id

        Bot.to_chat(chat_id, text, file_url)

    @staticmethod
    def get_updates(print_them=True):
        r = requests.get(Bot.base_url + "getUpdates")
        if print_them:
            print(r.text)
        return r.json()
