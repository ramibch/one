from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from etsyv3.util.auth import AuthHelper

from ..base.utils.telegram import Bot
from .models import Etsy


@login_required
def etsy_request_code(request):
    etsy = Etsy.load()
    auth = AuthHelper(
        etsy.keystring,
        etsy.redirect_uri,
        scopes=etsy.scopes.split(", "),
    )
    # 1. Call get_auth_code() on your AuthHelper - this will return an Etsy authentication URL
    url, code = auth.get_auth_code()
    # save in the etsy obj the generate properties
    etsy.code_verifier = auth.code_verifier
    etsy.state = auth.state
    etsy.code = code
    etsy.save()
    # 2. Go to that URL and authenticate with Etsy
    return redirect(url)


@login_required
def etsy_callback(request):
    # https://developers.etsy.com/documentation/tutorials/quickstart/#start-with-a-simple-express-server-application
    etsy = Etsy.load()

    # 3. Use the state and code params from the callback that Etsy will make to call set_authorization_code(code, state)
    # on an AuthHelper object initialised with the same the arguments passed to your first one (this callback is likely
    # to be in a completely new request context to the first - your original object may well no longer exist)
    state = request.GET["state"]
    code = request.GET["code"]

    Bot.to_admin(f"Etsy callback.\nstate={state}\ncode={code}")

    if state != etsy.state:
        # Before using an authorization code, validate that the state string in the response matches the state sent with the authorization code request.
        # If they do not match, halt authentication as the request is vulnerable to CSRF attacks.
        # If they match, make a note never to use that state again, and make your next authorization code request with a new state string.
        Bot.to_admin(f"Code from Etsy={state}\nCode requested={etsy.state}")
        return HttpResponse(status=403)

    auth = AuthHelper(
        etsy.keystring,
        etsy.redirect_uri,
        code_verifier=etsy.code_verifier,
        state=etsy.state,
    )
    auth.set_authorisation_code(code, state)
    # 4. You can then call get_access_token() on your AuthHelper object and you should get a dictionary returned
    # with the keys access_token, refresh_token and expires_at. These a required to create the EtsyAPI object.
    reponse = auth.get_access_token()
    etsy.access_token = reponse["access_token"]
    etsy.refresh_token = reponse["refresh_token"]
    etsy.expires_at = datetime.fromtimestamp(reponse["expires_at"])
    etsy.save()
    return HttpResponse("Logged in!")
