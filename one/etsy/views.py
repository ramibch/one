from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from etsyv3.util.auth import AuthHelper

from ..base.utils.telegram import Bot
from .models import App, UserShopAuth


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
    state = request.GET.get("state")
    code = request.GET.get("code")

    try:
        app = App.objects.get(state=state, code=state)
    except App.DoesNotExist:
        Bot.to_admin(f"Etsy callback. No App match.\nstate={state}\ncode={code}")
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


@login_required
def etsy_request_code_v2(request, id):
    app = get_object_or_404(App, id=id)
    auth_helper = AuthHelper(app.keystring, app.redirect_uri, scopes=app.scopes)
    # 1. Call get_auth_code() on your AuthHelper - this will return an Etsy authentication URL
    url, code = auth_helper.get_auth_code()
    # save in the etsy obj the generate properties
    UserShopAuth.objects.create(
        user=request.user,
        app=app,
        code=code,
        state=auth_helper.state,
        code_verifier=auth_helper.code_verifier,
    )
    # 2. Go to that URL and authenticate with Etsy
    return redirect(url)


@login_required
def etsy_callback_v2(request):
    # https://developers.etsy.com/documentation/tutorials/quickstart/#start-with-a-simple-express-server-application

    # 3. Use the state and code params from the callback that Etsy will make to call set_authorization_code(code, state)
    # on an AuthHelper object initialised with the same the arguments passed to your first one (this callback is likely
    # to be in a completely new request context to the first - your original object may well no longer exist)
    state = request.GET.get("state")
    code = request.GET.get("code")

    try:
        auth = UserShopAuth.objects.get(state=state, code=state, user=request.user)
    except UserShopAuth.DoesNotExist:
        Bot.to_admin(f"No UserShopAuth (Etsy) match.\nstate={state}\ncode={code}")
        return HttpResponseForbidden("Auth failed")

    auth_helper = AuthHelper(
        auth.app.keystring,
        auth.app.redirect_uri,
        code_verifier=auth.code_verifier,
        state=auth.state,
    )
    auth_helper.set_authorisation_code(code, state)
    # 4. You can then call get_access_token() on your AuthHelper object and you should get a dictionary returned
    # with the keys access_token, refresh_token and expires_at. These a required to create the EtsyAPI object.
    reponse = auth_helper.get_access_token()
    auth.access_token = reponse["access_token"]
    auth.refresh_token = reponse["refresh_token"]
    auth.expires_at = datetime.fromtimestamp(reponse["expires_at"])

    # TODO: Check if this issue is done: https://github.com/anitabyte/etsyv3/issues/26
    client_api = auth.get_api_client()
    url = "https://openapi.etsy.com/v3/application/users/me"
    data = requests.get(url, headers=client_api.session.headers).json()
    auth.etsy_user_id = data.get("user_id")
    auth.shop_id = data.get("shop_id")
    auth.save()
    return HttpResponse("Logged in!")
