from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from etsyv3.util.auth import AuthHelper

from ..base.utils.telegram import Bot
from .models import App


@login_required
def etsy_request_code(request, id):
    app = get_object_or_404(App, id=id)
    auth = AuthHelper(app.keystring, app.redirect_uri, scopes=app.scopes)
    # 1. Call get_auth_code() on your AuthHelper - this will return an Etsy authentication URL
    url, code = auth.get_auth_code()
    # save in the etsy obj the generate properties
    app.code_verifier = auth.code_verifier
    app.state = auth.state
    app.code = code
    app.save()
    # 2. Go to that URL and authenticate with Etsy
    return redirect(url)


@login_required
def etsy_callback(request):
    # https://developers.etsy.com/documentation/tutorials/quickstart/#start-with-a-simple-express-server-application

    # 3. Use the state and code params from the callback that Etsy will make to call set_authorization_code(code, state)
    # on an AuthHelper object initialised with the same the arguments passed to your first one (this callback is likely
    # to be in a completely new request context to the first - your original object may well no longer exist)
    state = request.GET["state"]
    code = request.GET["code"]

    try:
        app = App.objects.get(state=state, code=code)
    except App.DoesNotExist:
        Bot.to_admin(f"Etsy callback.\nstate={state}\ncode={code}")
        return HttpResponseForbidden()

    auth = AuthHelper(
        app.keystring,
        app.redirect_uri,
        code_verifier=app.code_verifier,
        state=app.state,
    )
    auth.set_authorisation_code(code, state)
    # 4. You can then call get_access_token() on your AuthHelper object and you should get a dictionary returned
    # with the keys access_token, refresh_token and expires_at. These a required to create the EtsyAPI object.
    reponse = auth.get_access_token()
    app.access_token = reponse["access_token"]
    app.refresh_token = reponse["refresh_token"]
    app.expires_at = datetime.fromtimestamp(reponse["expires_at"])
    app.save()
    return HttpResponse("Logged in!")
