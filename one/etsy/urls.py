from django.urls import path

from . import views

urlpatterns = [
    path("code/<int:id>", views.etsy_request_code, name="etsy_code"),
    path("callback", views.etsy_callback, name="etsy_callback"),
    path("refresh", views.RefreshView.as_view(), name="etsy_refresh"),
]
