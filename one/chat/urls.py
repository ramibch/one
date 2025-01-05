from django.urls import path

from .views import (
    ChatDetailView,
    MessageListView,
    chat_join,
    delete_message,
)

urlpatterns = [
    path("", ChatDetailView.as_view(), name="chat_detail"),
    path("messages/<str:chat_name>/", MessageListView.as_view(), name="chat_messages"),
    path("message-delete/<int:id>/", delete_message, name="chat_message_delete"),
    path("<str:name>", chat_join, name="chat_join"),
]
