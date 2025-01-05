import auto_prefetch
from auto_prefetch import ForeignKey, Model
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils.functional import cached_property

User = get_user_model()


class Chat(Model):
    name = models.CharField(max_length=128, unique=True)
    site = ForeignKey("sites.Site", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("chat", kwargs={"slug": self.name})

    @cached_property
    def url(self):
        return self.get_absolute_url()

    @cached_property
    def ws_url(self):
        return f"/ws/chat/{self.name}/"

    @cached_property
    def join_url(self):
        return reverse_lazy("chat_join", args=(self.name,))

    @cached_property
    def join_full_url(self):
        return self.site.main_host.name + self.join_url


class Message(auto_prefetch.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    chat = ForeignKey(Chat, on_delete=models.CASCADE)
    user = ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=512)
    deleted = models.BooleanField(default=False)

    @cached_property
    def time(self):
        return self.created_at.strftime("%H:%M")

    @cached_property
    def first_in_the_day(self):
        user_messages = self.user.message_set.filter(
            created_at__contains=self.created_at.date()
        )
        return user_messages.last() == self

    @cached_property
    def delete_url(self):
        return reverse_lazy("chat_message_delete", args=(self.id,))

    def __str__(self):
        return self.body[:40]

    class Meta(Model.Meta):
        ordering = ["-created_at"]
