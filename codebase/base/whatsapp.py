import requests
from django.conf import settings

BASE_URL = "https://graph.facebook.com/v21.0/"


def send_whatsapp_message(number: str, body_text: str, preview_url=False):
    """
    Send a notification to a number via Whatsapp
    https://developers.facebook.com/docs/whatsapp/cloud-api/messages/text-messages

    """
    url = BASE_URL + f"POST/{settings.WHATSAPP_BUSINESS_PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_API_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": str(number),
        "type": "text",
        "text": {"preview_url": preview_url, "body": body_text},
    }
    requests.post(url, data=data, headers=headers)
