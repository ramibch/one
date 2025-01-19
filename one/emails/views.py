import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from one.base.utils.telegram import Bot

from .models import DomainDNSError, MessageLinkClicked, MessageLoaded, PostalMessage


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

        case "MessageLinkClicked":
            MessageLinkClicked().save_from_payload(payload)

        case "MessageLoaded":
            MessageLoaded().save_from_payload(payload)

        case "DomainDNSError":
            DomainDNSError().save_from_payload(payload)

        case _:
            Bot.to_admin(f"Webhook endpoint to implemented:\n\n{data}")

    return HttpResponse()
