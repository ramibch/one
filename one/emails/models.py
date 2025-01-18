import tempfile
from copy import copy
from pathlib import Path

from auto_prefetch import ForeignKey, Model
from django.core.exceptions import ValidationError
from django.core.files.storage import storages
from django.core.mail import EmailMessage
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from one.base.utils.telegram import Bot


class Sender(Model):
    name = models.CharField(max_length=64)
    address = models.EmailField(max_length=64, unique=True)

    def __str__(self):
        return self.name_and_address

    @cached_property
    def name_and_address(self):
        return f"{self.name} <{self.address}>"

    def clean(self):
        super().clean()
        # TODO: Sender domain in Sites domain


class EmailMessageTemplate(Model):
    MIN_INTERVAL = timezone.timedelta(hours=8)
    MAX_INTERVAL = timezone.timedelta(days=365)
    MAX_TIME_RANGE = timezone.timedelta(days=3 * 365)
    sender = ForeignKey(Sender, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=128)
    reply_to = models.EmailField(max_length=64, null=True, blank=True)
    cc = models.EmailField(max_length=64, null=True, blank=True)
    body = models.TextField()
    remarks = models.TextField(null=True, blank=True)

    is_periodic = models.BooleanField(
        default=False,
        help_text=_("Email message will be send periodically."),
    )
    interval = models.DurationField(
        null=True,
        blank=True,
        help_text=_("Set when email message is periodic." + f" Min: {MIN_INTERVAL}"),
    )
    start_time = models.DateField(
        null=True,
        blank=True,
        help_text=_("Set when email message is periodic."),
    )
    stop_time = models.DateField(
        null=True,
        blank=True,
        help_text=_("Set when email message is periodic."),
    )

    def clean(self):
        super().clean()

        text = f"{self.subject}\n{self.body}"
        cleantext = text.replace("#var1", "").replace("#var2", "").replace("#var3", "")
        if "#" in cleantext:
            raise ValidationError(_("Tag '#' not recognised."), code="invalid")

        if self.is_periodic:
            if self.interval is None:
                raise ValidationError(_("Interval must be set."), code="invalid")

            if self.start_time is None:
                raise ValidationError(_("Start time must be set."), code="invalid")

            if self.stop_time is None:
                raise ValidationError(_("Stop time must be set."), code="invalid")

            if self.interval < self.MIN_INTERVAL:
                raise ValidationError(_("Interval too low."), code="invalid")

            if self.interval > self.MAX_INTERVAL:
                raise ValidationError(_("Interval too big."), code="invalid")

            if self.stop_time - self.start_time > self.MAX_TIME_RANGE:
                raise ValidationError(_("Time range too big."), code="invalid")

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

    def get_time_list(self) -> list | None:
        times = []
        if all((self.interval, self.start_time, self.stop_time, self.is_periodic)):
            next_time = self.start_time
            while next_time < self.stop_time:
                times.append(next_time)
                next_time += self.interval

        return times

    def __str__(self):
        return self.subject


class Attachment(Model):
    email_template = ForeignKey(EmailMessageTemplate, on_delete=models.CASCADE)
    file = models.FileField(upload_to="emails", storage=storages["private"])

    def __str__(self):
        return self.file.name


class Recipient(Model):
    email = ForeignKey(EmailMessageTemplate, on_delete=models.CASCADE)
    send_times = models.PositiveSmallIntegerField(default=0, editable=False)
    sent_on = models.DateTimeField(null=True, blank=True, editable=False)
    to_address = models.EmailField(max_length=128)
    var_1 = models.CharField(max_length=64, null=True, blank=True)
    var_2 = models.CharField(max_length=64, null=True, blank=True)
    var_3 = models.CharField(max_length=64, null=True, blank=True)
    draft = models.BooleanField(default=False)

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

    @cached_property
    def email_body(self):
        return self.text_replace(self.email.body)

    @cached_property
    def email_subject(self):
        return self.text_replace(self.email.subject)

    @cached_property
    def allow_to_send_email(self):
        common = all(
            (
                "#var" not in self.email_body,
                "#var" not in self.email_subject,
                not self.draft,
                self.email.sender is not None,
            )
        )

        if self.email.is_periodic:
            expression = "%Y_%m_%d_%H_%M"
            strnow = timezone.now().strftime(expression)
            strtimes = [t.strftime(expression) for t in self.email.get_time_list()]
            extra = strnow in strtimes
        else:
            extra = self.send_times < 1

        return common and extra

    def send_email(self, fail_silently=False):
        if self.allow_to_send_email:
            reply_to = self.email.reply_to
            cc = self.email.cc

            msg = EmailMessage(
                subject=self.email_subject(),
                body=self.email_body(),
                from_email=self.email.sender.name_and_address,
                to=[self.to_address],
                cc=None if cc is None else [cc],
                reply_to=None if reply_to is None else [reply_to],
            )

            local_attachments = self.email.get_local_attachments()
            for local_attachment in local_attachments:
                msg.attach_file(local_attachment)

            # Send the email
            msg.send(fail_silently=fail_silently)
            self.send_times += self.send_times
            self.sent_on = timezone.now()
            self.save()

        else:
            msg = f"Email {self.email} not allowed to send to {self.to_address}"
            Bot.to_admin(msg)


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

    class Meta(Model.Meta):
        verbose_name = "Postal: MessageSent"
        verbose_name_plural = "Postal: MessageSent"

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

    class Meta(Model.Meta):
        verbose_name = "Postal: MessageLinkClicked"
        verbose_name_plural = "Postal: MessageLinkClicked"

    def save_from_payload(self, payload: dict):
        please_implement_save_from_payload("MessageLinkClicked", payload)


class MessageLoaded(Model):
    """
    https://docs.postalserver.io/developer/webhooks#message-loadedopened-event
    """

    class Meta(Model.Meta):
        verbose_name = "Postal: MessageLoaded"
        verbose_name_plural = "Postal: MessageLoaded"

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

    class Meta(Model.Meta):
        verbose_name = "Postal: DomainDNSError"
        verbose_name_plural = "Postal: DomainDNSError"

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
