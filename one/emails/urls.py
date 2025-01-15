from django.urls import path

from .views import postal_webhook

urlpatterns = [
    path("webhook/", postal_webhook, name="email_postal_webhook"),
]
