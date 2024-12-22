from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from ..base.utils.telegram import Bot
from .models import Chat, Message


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat

    def get_object(self, queryset=...):
        site = self.request.site
        username = self.request.user.username

        try:
            chat = Chat.objects.get(name=username)
        except Chat.DoesNotExist:
            chat = Chat.objects.create(name=username, site=site)
            Bot.to_admin(f"💬 New chat: {chat.join_url}")

        return chat


class MessageListView(LoginRequiredMixin, ListView):
    context_object_name = "chat_messages"
    model = Message

    def get_queryset(self):
        chat_name = self.kwargs.get("chat_name")
        return Message.objects.filter(chat__name=chat_name, deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["chat"] = Chat.objects.get(name=self.kwargs.get("chat_name"))
        return context


@login_required
@require_http_methods(["DELETE"])
def delete_message(request, id):
    Message.objects.filter(user=request.user, id=id).update(deleted=True)
    return HttpResponse(status=200)


@login_required
def chat_join(request, name):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    chat = Chat.objects.get_or_create(name=name)[0]
    messages = chat.message_set.all()
    context = {"chat": chat, "chat_messages": messages, "user": request.user}
    return render(request, "chat/chat_detail.html", context)
