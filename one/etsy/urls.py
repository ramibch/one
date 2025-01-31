from django.urls import path

from . import views

urlpatterns = [
    path("code/<int:id>", views.etsy_request_code, name="etsy_code"),
    path("callback", views.etsy_callback, name="etsy_callback"),
    path("v2-code/<int:id>", views.etsy_request_code_v2, name="etsy_code_v2"),
    path("v2-callback", views.etsy_callback_v2, name="etsy_callback_v2"),
]
