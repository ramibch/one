import ssl

import requests
from django.conf import settings


class Bot:
    ssl._create_default_https_context = ssl._create_unverified_context
    BASE_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_API_KEY}/"

    def to_chat(chat_id: str, text: str):
        """Send text message to a chat"""
        parameters = {"chat_id": chat_id, "text": text, "disable_web_page_preview": True}
        try:
            requests.get(Bot.BASE_URL + "sendMessage", params=parameters)
        except Exception:
            raise Exception

    def to_admin(text: str):
        """Send text message to the admin"""
        chat_id = settings.TELEGRAM_ADMIN_CHAT_ID
        Bot.to_chat(chat_id=chat_id, text=text)

    def to_group(group_id, text, file_url=None):
        """Send text and optionally an image to a group"""
        chat_id = "@" + group_id if not group_id.startswith("@") else group_id

        if file_url:
            parameters = {"chat_id": chat_id, "caption": text, "photo": file_url}
            r = requests.get(Bot.BASE_URL + "sendPhoto", params=parameters)
            if r.status_code != 200:
                parameters = {"chat_id": chat_id, "caption": text, "document": file_url}
                requests.get(Bot.BASE_URL + "sendDocument", params=parameters)
        else:
            Bot.to_chat(chat_id, text)
