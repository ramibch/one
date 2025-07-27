from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect

from one.bot import Bot

from .linkedin import LinkedinClient


@login_required
def linkedin_request_code(request):
    url = LinkedinClient.get_authorization_url()
    return redirect(url)


@login_required
def linkedin_callback(request):
    Bot.to_admin(str(request.body))
    Bot.to_admin(str(request.GET))
    return HttpResponse("ok...")
