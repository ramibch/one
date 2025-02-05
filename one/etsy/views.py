from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from etsyv3.util.auth import AuthHelper
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

from one.base.utils.telegram import Bot

from .models import App, UserShopAuth


@login_required
def etsy_request_code(request, id):
    app = get_object_or_404(App, id=id)
    auth_helper = AuthHelper(
        keystring=app.keystring,
        redirect_uri=app.redirect_uri,
        scopes=app.scopes,
    )
    # 1. Call get_auth_code() on your AuthHelper - this will return an Etsy authentication URL
    url, state = auth_helper.get_auth_code()
    # save in the etsy obj the generate properties
    UserShopAuth.objects.create(
        user=request.user,
        app=app,
        code=state,
        state=auth_helper.state,
        code_verifier=auth_helper.code_verifier,
        scopes=app.scopes,  # store the selected scopes
    )
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
        userauth = UserShopAuth.objects.get(code=state, state=state, user=request.user)
    except UserShopAuth.DoesNotExist:
        Bot.to_admin(f"No UserShopAuth (Etsy) match.\nstate={state}\ncode={code}")
        return HttpResponseForbidden("Auth failed, contact admin")

    auth_helper = AuthHelper(
        userauth.app.keystring,
        userauth.app.redirect_uri,
        code_verifier=userauth.code_verifier,
        state=userauth.state,
        scopes=userauth.scopes,
    )
    auth_helper.set_authorisation_code(code, state)
    # 4. You can then call get_access_token() on your AuthHelper object and you should get a dictionary returned
    # with the keys access_token, refresh_token and expires_at. These a required to create the EtsyAPI object.
    try:
        response = auth_helper.get_access_token()
    except InvalidGrantError as e:
        Bot.to_admin(f"Etsy Auth error ({userauth.id}):{e}")
        return HttpResponseForbidden("Auth failed, contact admin.")

    userauth.access_token = response["access_token"]
    userauth.refresh_token = response["refresh_token"]
    userauth.expires_at = datetime.fromtimestamp(response["expires_at"])

    # Get shop_id and user_id if not assigned
    if None in (userauth.shop_id, userauth.etsy_user_id):
        client_api = userauth.get_api_client()
        data = client_api.get_me()
        userauth.etsy_user_id = data.get("user_id")
        userauth.shop_id = data.get("shop_id")

    userauth.save()

    return HttpResponse("Logged in!")
