from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect

from .models import LinkedinAuth
from .utils import get_linkedin_access_from_code


@login_required
def linkedin_callback(request):
    state = request.GET.get("state")
    code = request.GET.get("code")
    if not state or not code:
        return HttpResponseBadRequest("Missing state or code in callback URL")

    try:
        auth = LinkedinAuth.objects.get(state=state)
    except LinkedinAuth.DoesNotExist:
        return HttpResponse(f"Linkedin channel with auth state {state} not found in db")

    try:
        access_data = get_linkedin_access_from_code(code)
        auth.update_values(access_data, code=code)
    except Exception as e:
        return HttpResponse(f"Failed to update auth object ({auth.pk}): {str(e)}")

    return redirect(auth.admin_url)
