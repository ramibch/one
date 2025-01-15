from auto_prefetch import Model
from django.db import models


class MessageSent(Model):
    status = models.CharField(max_length=128, default="")
    details = models.CharField(max_length=512, default="")
    output = models.CharField(max_length=512, default="")
    time = models.FloatField(default=0.0)
    sent_with_ssl = models.BooleanField(default=False)
    timestamp = models.FloatField(null=True)
    message_int_id = models.PositiveIntegerField(null=True)
    message_token = models.CharField(max_length=128, default="")
    message_direction = models.CharField(max_length=128, default="")
    message_id = models.CharField(max_length=128, default="")
    message_to = models.EmailField()
    message_from = models.EmailField()
    message_subject = models.CharField(max_length=128, default="")
    message_timestamp = models.FloatField(null=True)
    message_spam_status = models.CharField(max_length=128, default="")
    message_tag = models.CharField(max_length=128, default="")

    def __str__(self):
        return f"[{self.message_to}] {self.message_subject}"
