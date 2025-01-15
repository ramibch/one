from auto_prefetch import Model
from django.db import models

from one.base.utils.telegram import Bot


def please_implement_this(model_name, payload):
    Bot.to_admin(f"Please implement {model_name}.save_from_payload\n\n{str(payload)}")


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

    def save_from_payload(self, payload: dict):
        """
        {'event': 'MessageSent',
         'timestamp': 1736982212.445696,
         'payload': {'message': {'id': 74,
           'token': 'ojaKwqL7ACULMl4D',
           'direction': 'outgoing',
           'message_id': '173698220910.787872.8328578722038804350@msi',
           'to': 'ramiboutas@hotmail.com',
           'from': 'me@ramib.ch',
           'subject': 'Hello Rami',
           'timestamp': 1736982209.2173178,
           'spam_status': 'NotChecked',
           'tag': None},
          'status': 'Sent',
          'details': 'Message for ramiboutas@hotmail.com accepted by 52.101.68.38:25 (hotmail-com.olc.protection.outlook.com)',
          'output': '250 2.6.0 <173698220910.787872.8328578722038804350@msi> [InternalId=29072633627620, Hostname=DU0P192MB2073.EURP192.PROD.OUTLOOK.COM] 9803 bytes in 0.195, 49.066 KB/sec Queued mail for delivery -> 250 2.1.5',
          'sent_with_ssl': True,
          'timestamp': 1736982212.436434,
          'time': 0.74},
         'uuid': '5e57784f-0be1-4281-b90a-887d496cadae'}
        """
        please_implement_this("MessageSent", payload)

    def __str__(self):
        return f"[{self.message_to}] {self.message_subject}"


class MessageLinkClicked(Model):
    def save_from_payload(self, payload: dict):
        please_implement_this("MessageLinkClicked", payload)


class MessageLoaded(Model):
    def save_from_payload(self, payload: dict):
        please_implement_this("MessageLoaded", payload)


class DomainDNSError(Model):
    pass

    def save_from_payload(self, payload: dict):
        please_implement_this("DomainDNSError", payload)
