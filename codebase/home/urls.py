from django.urls import path

from .views import home

urlpatterns = [
    # Home
    path("", home, name="home"),
]
