import os
import tempfile
from copy import copy
from pathlib import Path

from auto_prefetch import ForeignKey, Model
from django.core.files.storage import storages
from django.core.mail import EmailMessage
from django.db import models
from django.utils import timezone

from one.base.utils.telegram import Bot


class MessageTemplate(Model):
    address_from = models.EmailField(max_length=64)
    subject = models.CharField(max_length=128)
    reply_to = models.EmailField(max_length=64, null=True, blank=True)
    cc = models.EmailField(max_length=64, null=True, blank=True)
    body = models.TextField()
    var1_meaning = models.CharField(max_length=64, null=True, blank=True)
    var2_meaning = models.CharField(max_length=64, null=True, blank=True)
    var3_meaning = models.CharField(max_length=64, null=True, blank=True)

    def get_local_attachments(self):
        local_attachments = []
        for attachment in self.attachment_set.all():
            fileb = attachment.file.storage.open(attachment.file.name, "rb").read()
            with tempfile.TemporaryDirectory(delete=False) as tmpdirname:
                local_attachment = f"{tmpdirname}/{attachment.file.name}"
                Path(local_attachment).parent.mkdir(exist_ok=True, parents=True)
                with open(local_attachment, "wb") as f:
                    f.write(fileb)
                    local_attachments.append(local_attachment)

        return local_attachments

    def __str__(self):
        return self.subject


class Attachment(Model):
    email_template = ForeignKey(MessageTemplate, on_delete=models.CASCADE)
    file = models.FileField(upload_to="emails", storage=storages["private"])

    def __str__(self):
        return self.file.name


class Recipient(Model):
    email_template = ForeignKey(MessageTemplate, on_delete=models.CASCADE)
    subject = models.CharField(max_length=128)
    body = models.TextField()
    to_address = models.EmailField(max_length=128)
    var_1 = models.CharField(max_length=64, null=True, blank=True)
    var_2 = models.CharField(max_length=64, null=True, blank=True)
    var_3 = models.CharField(max_length=64, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    draft = models.BooleanField(default=False)
    email_sent_on = models.DateTimeField(null=True, blank=True, editable=False)
    email_sent = models.BooleanField(default=False, editable=False)

    def __str__(self) -> str:
        return self.to_address

    def text_replace(self, text: str):
        replacements = {
            "#var1": self.var_1,
            "#var2": self.var_2,
            "#var3": self.var_3,
        }
        text_copy = copy(text)
        for var_tag, var_value in replacements.items():
            text_copy = text_copy.replace(var_tag, var_value or var_tag)
        return text_copy

    def get_email_body(self):
        return self.text_replace(self.email_template.body)

    def get_email_subject(self):
        return self.text_replace(self.email_template.subject)

    def allow_to_send_email(self):
        return all(
            (
                "#var" not in self.get_email_body(),
                "#var" not in self.get_email_subject(),
                not self.draft,
                not self.email_sent,
            )
        )

    def send_email(self):
        if not self.allow_to_send_email():
            Bot.to_admin(
                f"Email {self.email_template} not allowed to send to {self.to_address}"
            )
            return
        reply_to = self.email_template.reply_to
        cc = self.email_template.cc

        msg = EmailMessage(
            subject=self.get_email_subject(),
            body=self.get_email_body(),
            from_email=self.email_template.address_from,
            to=[self.to_address],
            cc=None if cc is None else [cc],
            reply_to=None if reply_to is None else [reply_to],
        )

        local_attachments = self.email_template.get_local_attachments()
        for local_attachment in local_attachments:
            msg.attach_file(local_attachment)

        try:
            msg.send(fail_silently=False)
            self.email_sent = True
            self.email_sent_on = timezone.now()
            self.save()
        except Exception as e:
            Bot.to_admin(f"Email Error {self.email_template} :{e}")

        # Remove temporary files
        for local_attachment in local_attachments:
            os.unlink(local_attachment)


# Postal models
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
