from django.urls import path

from .views import change_client_theme

urlpatterns = [
    path("change-theme", change_client_theme, name="client_theme"),
]
