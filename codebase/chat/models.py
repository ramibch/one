import auto_prefetch
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from users.models import User


class Chat(auto_prefetch.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("chat", kwargs={"slug": self.name})

    @cached_property
    def url(self):
        return self.get_absolute_url()

    @cached_property
    def ws_url(self):
        return f"/ws/chat/{self.name}/"


class Message(auto_prefetch.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    chat = auto_prefetch.ForeignKey(Chat, on_delete=models.CASCADE)
    author = auto_prefetch.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=512)

    def __str__(self):
        return str(self.body)
