from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from etsyv3.util.auth import AuthHelper
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

from one.base.utils.telegram import Bot

from .models import App, EtsyAuth, Shop


@login_required
def etsy_request_code(request):
    keystring = request.GET.get("keystring")
    app = get_object_or_404(App, keystring=keystring)
    auth_helper = AuthHelper(
        keystring=app.keystring,
        redirect_uri=app.redirect_uri,
        scopes=app.scopes,
    )
    # 1. Call get_auth_code() on your AuthHelper - this will return an Etsy authentication URL
    url, state = auth_helper.get_auth_code()
    # save in the etsy obj the generate properties
    EtsyAuth.objects.create(
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
    # 'Referer': 'https://www.etsy.com/'
    if not "etsy.com" in request.headers.get("Referer", ""):
        # Refresh o user tried to change the language
        return etsy_dashboard(request)

    # https://developers.etsy.com/documentation/tutorials/quickstart/#start-with-a-simple-express-server-application

    # 3. Use the state and code params from the callback that Etsy will make to call set_authorization_code(code, state)
    # on an AuthHelper object initialised with the same the arguments passed to your first one (this callback is likely
    # to be in a completely new request context to the first - your original object may well no longer exist)
    state = request.GET.get("state")
    code = request.GET.get("code")

    try:
        etsy_auth = EtsyAuth.objects.get(code=state, state=state, user=request.user)
    except EtsyAuth.DoesNotExist:
        Bot.to_admin(f"No UserShopAuth (Etsy) match.\nstate={state}\ncode={code}")
        return HttpResponseForbidden("Auth failed, contact admin")

    auth_helper = AuthHelper(
        etsy_auth.app.keystring,
        etsy_auth.app.redirect_uri,
        code_verifier=etsy_auth.code_verifier,
        state=etsy_auth.state,
        scopes=etsy_auth.scopes,
    )
    auth_helper.set_authorisation_code(code, state)
    # 4. You can then call get_access_token() on your AuthHelper object and you should get a dictionary returned
    # with the keys access_token, refresh_token and expires_at. These a required to create the EtsyAPI object.
    try:
        response = auth_helper.get_access_token()
    except InvalidGrantError as e:
        Bot.to_admin(f"Etsy Auth error ({etsy_auth.id}):{e}")
        return HttpResponseForbidden("Auth failed, contact admin.")

    etsy_auth.access_token = response["access_token"]
    etsy_auth.refresh_token = response["refresh_token"]
    etsy_auth.expires_at = datetime.fromtimestamp(response["expires_at"])

    # Get shop_id and user_id if not assigned
    if None in (etsy_auth.shop_id, etsy_auth.etsy_user_id):
        client_api = etsy_auth.get_api_client()
        data = client_api.get_me()
        etsy_auth.etsy_user_id = data.get("user_id")
        etsy_auth.shop_id = data.get("shop_id")
    
    etsy_auth.save()
    shop = Shop(etsy_auth=etsy_auth)
    shop.update_from_etsy()
    return render(request, "etsy/after_callback.html", {"etsy_auth": etsy_auth})


def etsy_dashboard(request):
    return HttpResponse("TODO!")