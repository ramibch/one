import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from one.base.utils.telegram import Bot

from .models import DomainDNSError, MessageLinkClicked, MessageLoaded, PostalMessage


def process_bounce_message(original, bounce):
    msg = (
        "📧⚠️ New bounce message\n\n"
        f"Original message:\n"
        f"ID: {original.get("id")}\n"
        f"Direction: {original.get("direction")}\n"
        f"Subject: {original.get("subject")}\n"
        f"From: {original.get("from")}\n"
        f"To: {original.get("to")}\n"
        f"Spam Status: {original.get("spam_status")}\n\n"
        f"Bounce message:\n"
        f"ID: {bounce.get("id")}\n"
        f"Direction: {bounce.get("direction")}\n"
        f"Subject: {bounce.get("subject")}\n"
        f"From: {bounce.get("from")}\n"
        f"To: {bounce.get("to")}\n"
        f"Spam Status: {bounce.get("spam_status")}\n"
    )
    Bot.to_admin(msg)


@csrf_exempt
@require_POST
def postal_webhook(request):
    signature = request.headers.get("X-Postal-Signature-Kid", "")
    if signature != settings.POSTAL_SIGNATURE_KID:
        return HttpResponseForbidden()

    data = json.loads(request.body.decode("utf-8"))
    event = data.get("event")
    payload = data.get("payload", {})

    match event:
        case "MessageSent":
            PostalMessage().save_from_payload(payload)

        case "MessageDelayed":
            obj = PostalMessage()
            obj.delayed = True
            obj.save_from_payload(payload)

        case "MessageHeld":
            obj = PostalMessage()
            obj.held = True
            obj.save_from_payload(payload)
        case "MessageDeliveryFailed":
            obj = PostalMessage()
            obj.delivery_failed = True
            obj.save_from_payload(payload)

        case "MessageBounced":
            original = data.get("original_message")
            bounce = data.get("bounce")
            process_bounce_message(original, bounce)

        case "MessageLinkClicked":
            MessageLinkClicked().save_from_payload(payload)

        case "MessageLoaded":
            MessageLoaded().save_from_payload(payload)

        case "DomainDNSError":
            DomainDNSError().save_from_payload(payload)

        case _:
            Bot.to_admin(f"Webhook endpoint to implemented:\n\n{data}")

    return HttpResponse()
