from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from .models import Chat


@login_required
def chat_detail(request):
    chat = Chat.objects.get_or_create(name=request.user.username)[0]
    messages = chat.message_set.all()[:30]
    context = {"chat": chat, "chat_messages": messages}
    return render(request, "chat_detail.html", context)


@login_required
def chat_join(request, name):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    chat = Chat.objects.get_or_create(name=name)[0]
    messages = chat.message_set.all()[:30]
    context = {"chat": chat, "chat_messages": messages}
    return render(request, "chat_detail.html", context)
