from django.urls import path

from . import views

urlpatterns = [
    # Auth management
    path("linkedin/code/", views.linkedin_request_code, name="linkedin_code"),
    path("linkedin/callback/", views.linkedin_callback, name="linkedin_callback"),
]
