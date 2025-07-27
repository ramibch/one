from django.urls import path

from .views import linkedin_callback

urlpatterns = [
    # Auth management
    path("linkedin/callback/", linkedin_callback, name="linkedin_callback"),
]
