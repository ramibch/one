from django.urls import path

from . import views

urlpatterns = [
    path("calendar/", views.test_calendar, name="tex-calendar"),
]
