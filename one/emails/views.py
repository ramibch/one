import json

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import (
    PostalDomainDNSError,
    PostalMessage,
    PostalMessageLinkClicked,
    PostalMessageLoaded,
)


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
            PostalMessage.save_from_payload(payload)

        case "MessageDelayed":
            PostalMessage.save_from_payload(payload, delayed=True)

        case "MessageHeld":
            PostalMessage.save_from_payload(payload, held=True)

        case "MessageDeliveryFailed":
            PostalMessage.save_from_payload(payload, delivery_failed=True)

        case "MessageBounced":
            pass

        case "MessageLinkClicked":
            PostalMessageLinkClicked().save_from_payload(payload)

        case "MessageLoaded":
            PostalMessageLoaded().save_from_payload(payload)

        case "DomainDNSError":
            PostalDomainDNSError().save_from_payload(payload)

        case _:  # for messages
            return HttpResponse("Message received!")

    # data_yaml = yaml.dump(data, default_flow_style=False)
    # msg = f"📧 New Postal webhook event\n\n{data_yaml}"
    # Bot.to_admin(msg)

    return HttpResponse("Processed!")
