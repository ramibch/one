import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST


@require_POST
def postal_webhook(request):
    with open(settings.BASE_DIR / "postal_post.txt", "w") as f:
        f.write(json.dumps(request.POST))

    with open(settings.BASE_DIR / "postal_meta.txt", "w") as f:
        f.write(json.dumps(request.META))

    return HttpResponse()
