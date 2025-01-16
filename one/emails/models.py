from auto_prefetch import Model
from django.db import models

from one.base.utils.telegram import Bot


def please_implement_save_from_payload(model_name, payload):
    Bot.to_admin(f"Please implement {model_name}.save_from_payload\n\n{str(payload)}")


class MessageSent(Model):
    """
    https://docs.postalserver.io/developer/webhooks#message-status-events
    """

    status = models.CharField(max_length=128, null=True)
    details = models.CharField(max_length=512, null=True)
    output = models.CharField(max_length=512, null=True)
    time = models.FloatField(default=0.0)
    sent_with_ssl = models.BooleanField(default=False)
    timestamp = models.FloatField(null=True)
    message_token = models.CharField(max_length=128, null=True)
    message_direction = models.CharField(max_length=128, null=True)
    message_id = models.CharField(max_length=128, null=True)
    message_from = models.EmailField()
    message_to = models.EmailField()
    message_subject = models.CharField(max_length=128, null=True)
    message_timestamp = models.FloatField(null=True)
    message_spam_status = models.CharField(max_length=128, null=True)
    message_tag = models.CharField(max_length=128, null=True)

    def save_from_payload(self, payload: dict):
        message: dict = payload.get("message", {})

        # Message attrs
        self.message_token = message.get("token")
        self.message_direction = message.get("direction")
        self.message_id = message.get("message_id")
        self.message_to = message.get("to")
        self.message_from = message.get("from")
        self.message_subject = message.get("subject")
        self.message_timestamp = message.get("timestamp")
        self.message_spam_status = message.get("spam_status")
        self.message_tag = message.get("tag")

        # Output
        self.output = payload.get("output")
        # Status
        self.status = payload.get("status")
        # Details
        self.details = payload.get("details")
        # Send with SSL
        self.sent_with_ssl = payload.get("sent_with_ssl")
        # Time
        self.time = payload.get("time")
        # Timestamp
        self.timestamp = payload.get("timestamp")

        if self.message_id:
            self.save()

    def __str__(self):
        return f"[{self.message_to}] {self.message_subject}"


class MessageLinkClicked(Model):
    """
    https://docs.postalserver.io/developer/webhooks#message-click-event
    """

    def save_from_payload(self, payload: dict):
        please_implement_save_from_payload("MessageLinkClicked", payload)


class MessageLoaded(Model):
    """
    https://docs.postalserver.io/developer/webhooks#message-loadedopened-event
    """

    def save_from_payload(self, payload: dict):
        please_implement_save_from_payload("MessageLoaded", payload)


class DomainDNSError(Model):
    """
    https://docs.postalserver.io/developer/webhooks#dns-error-event
    """

    domain = models.CharField(max_length=128, null=True)
    uuid = models.CharField(max_length=128, null=True)
    dns_checked_at = models.FloatField(default=0.0)
    spf_status = models.CharField(max_length=128, null=True)
    spf_error = models.CharField(max_length=256, null=True)
    dkim_status = models.CharField(max_length=128, null=True)
    dkim_error = models.CharField(max_length=256, null=True)
    mx_status = models.CharField(max_length=128, null=True)
    mx_error = models.CharField(max_length=256, null=True)
    return_path_status = models.CharField(max_length=128, null=True)
    return_path_error = models.CharField(max_length=256, null=True)

    def save_from_payload(self, payload: dict):
        self.domain = payload.get("domain")
        self.uuid = payload.get("uuid")
        self.dns_checked_at = payload.get("dns_checked_at")
        self.spf_status = payload.get("spf_status")
        self.spf_error = payload.get("spf_error")
        self.dkim_status = payload.get("dkim_status")
        self.dkim_error = payload.get("dkim_error")
        self.mx_status = payload.get("mx_status")
        self.mx_error = payload.get("mx_error")
        self.return_path_status = payload.get("return_path_status")
        self.return_path_error = payload.get("return_path_error")

        if self.domain and self.uuid:
            self.save()

    def __str__(self):
        return f"[{self.uuid}] {self.domain}"
