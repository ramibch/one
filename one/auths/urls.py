from django.urls import path

from . import views

urlpatterns = [
    # etsy
    path("etsy/code", views.etsy_request_code, name="etsy-code"),
    path("etsy/callback", views.etsy_callback, name="etsy-callback"),
]
