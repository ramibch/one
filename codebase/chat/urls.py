from django.urls import path

from . import views

urlpatterns = [
    path("", views.chat_detail, name="chat-detail"),
    path("<str:name>", views.chat_join, name="chat-join"),
]
