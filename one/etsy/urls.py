from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.etsy_dashboard, name="etsy_dashboard"),
    # Auth management
    path("code", views.etsy_request_code, name="etsy_code"),
    path("callback", views.etsy_callback, name="etsy_callback"),
    # API
    path("api/", include("one.etsy.api.urls")),
]
