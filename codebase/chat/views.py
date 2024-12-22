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
        chat, created = Chat.objects.get_or_create(
            name=self.request.user.username,
            site=self.request.site,
        )

        if created:
            Bot.to_admin(f"💬 New chat: {chat.join_url}")
        return chat


class MessageListView(LoginRequiredMixin, ListView):
    context_object_name = "chat_messages"
    model = Message

    def get_queryset(self):
        username = self.request.user.username
        return self.model.objects.filter(chat__name=username, deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
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
