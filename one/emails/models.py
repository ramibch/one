from copy import copy
from datetime import datetime, timedelta

from auto_prefetch import ForeignKey, Model
from django.core.exceptions import ValidationError
from django.core.files.storage import storages
from django.core.mail import EmailMessage
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from one.base.utils.telegram import Bot
from one.base.utils.tmp import TmpFile
from one.sites.models import Site


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
        domain = self.address.split("@")[1]
        if not Site.objects.filter(domain=domain).exists():
            raise ValidationError(_("Domain does not match any sites."), code="invalid")


class TemplateMessage(Model):
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
    start_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Set when email message is periodic."),
    )
    stop_time = models.DateTimeField(
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

    @cached_property
    def local_attachments(self):
        return [TmpFile(attachment.file).path for attachment in self.templateattachment_set.all()]

    def send_periodic_email_now(self) -> bool:
        # Validate required attributes
        if not all((self.interval, self.start_time, self.stop_time, self.is_periodic)):
            return False

        # Get the current time rounded to the nearest minute
        current_time = now().replace(second=0, microsecond=0)

        # Validate that current time is within the range
        if not (self.start_time <= current_time <= self.stop_time):
            return False

        # Calculate if the current time matches the periodic interval
        return (current_time - self.start_time) % self.interval == timedelta(0)

    def __str__(self):
        return self.subject


class TemplateAttachment(Model):
    def get_directory(self, filename):
        return f"emails/{self.email.id}/{filename}"

    email = ForeignKey(TemplateMessage, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_directory, storage=storages["private"])

    def __str__(self):
        return str(self.file)


class TemplateRecipient(Model):
    email = ForeignKey(TemplateMessage, on_delete=models.CASCADE)
    send_times = models.PositiveSmallIntegerField(default=0, editable=False)
    sent_on = models.DateTimeField(null=True, blank=True, editable=False)
    to_address = models.EmailField(max_length=128)
    var_1 = models.CharField(max_length=64, null=True, blank=True)
    var_2 = models.CharField(max_length=64, null=True, blank=True)
    var_3 = models.CharField(max_length=64, null=True, blank=True)
    draft = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True) 

    class Meta(Model.Meta):
        unique_together = ("email", "to_address")

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
            extra = self.email.send_periodic_email_now()
        else:
            extra = self.send_times == 0
        return common and extra

    def send_email(self, fail_silently=False):
        if self.allow_to_send_email():
            reply_to = self.email.reply_to
            cc = self.email.cc

            msg = EmailMessage(
                subject=self.email_subject,
                body=self.email_body,
                from_email=self.email.sender.name_and_address,
                to=[self.to_address],
                cc=None if cc is None else [cc],
                reply_to=None if reply_to is None else [reply_to],
            )

            for local_attachment in self.email.local_attachments:
                msg.attach_file(local_attachment)

            # Send the email
            msg.send(fail_silently=fail_silently)
            self.send_times = self.send_times + 1
            self.sent_on = timezone.now()
            self.save()


# Postal models
def please_implement_save_from_payload(model_name, payload):
    Bot.to_admin(f"Please implement {model_name}.save_from_payload\n\n{str(payload)}")


class PostalMessage(Model):
    """
    https://docs.postalserver.io/developer/webhooks#message-status-events
    """

    POSTAL_URL = "https://postal.ramib.ch/org/ramib-ch/servers/ramib-ch/messages/{}/plain"

    status = models.CharField(max_length=128, null=True)
    details = models.CharField(max_length=512, null=True)
    output = models.CharField(max_length=512, null=True)
    time = models.FloatField(default=0.0)
    sent_with_ssl = models.BooleanField(default=False)
    timestamp = models.FloatField(null=True)
    token = models.CharField(max_length=128, null=True)
    direction = models.CharField(max_length=128, null=True)
    large_id = models.CharField(max_length=128, null=True)
    mail_from = models.EmailField()
    mail_to = models.EmailField()
    subject = models.CharField(max_length=256, null=True)
    spam_status = models.CharField(max_length=128, null=True)
    tag = models.CharField(max_length=128, null=True)

    # flags
    delayed = models.BooleanField(null=True, default=False)
    held = models.BooleanField(null=True, default=False)
    delivery_failed = models.BooleanField(null=True, default=False)

    # own fields
    received_at = models.DateTimeField(null=True)
    message_dict = models.JSONField(null=True)

    @cached_property
    def url(self):
        return self.POSTAL_URL.format(self.id)

    class Meta(Model.Meta):
        verbose_name = "Postal: Message"
        verbose_name_plural = "Postal: Messages"

    def save_from_payload(self, payload: dict):
        message: dict = payload.get("message", {})
        # ID
        # Message attrs
        self.id = message.get("id")
        self.token = message.get("token")
        self.direction = message.get("direction")
        self.large_id = message.get("message_id")
        self.mail_to = message.get("to")
        self.mail_from = message.get("from")
        self.subject = message.get("subject")
        self.spam_status = message.get("spam_status")
        self.tag = message.get("tag")

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

        # Own fields
        self.message_dict = message
        
        if self.timestamp:
            dt = datetime.fromtimestamp(int(self.timestamp))
            self.received_at = timezone.make_aware(dt, timezone.get_current_timezone())
        
        self.save()

    def __str__(self):
        return f"[{self.id}] {self.subject}"[:40]


class PostalReplyMessage(Model):
    def get_file_path(self, filename):
        return f"emails/replies/{self.id}/{filename}"

    postal_message = ForeignKey(PostalMessage, on_delete=models.CASCADE)
    body = models.TextField()
    replied = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    replied_on = models.DateTimeField(null=True, blank=True, editable=False)
    file = models.FileField(
        upload_to=get_file_path, storage=storages["private"], null=True, blank=True
    )

    @cached_property
    def subject(self):
        return f"Re: {self.postal_message.subject}"

    @cached_property
    def mail_to(self):
        return self.postal_message.mail_from

    @cached_property
    def mail_from(self):
        return self.postal_message.mail_to

    @cached_property
    def local_file(self):
        if not self.file.name:
            raise ValueError("Attachment field cannot be null")
        return TmpFile(self.file).path

    @cached_property
    def mail_headers(self):
        return {
            "References": self.postal_message.large_id,
            "In-Reply-To": self.postal_message.large_id,
        }

    @cached_property
    def sender(self) -> Sender:
        try:
            return Sender.objects.get(address=self.mail_from)
        except Sender.DoesNotExist:
            name = self.mail_from.split("@")[0]
            Bot.to_admin(f"⚠️ Rename sender name: {self.mail_from}")
            return Sender.objects.create(address=self.mail_from, name=name)

    def reply(self, fail_silently=False):
        if self.replied:
            return

        msg = EmailMessage(
            subject=self.subject,
            body=self.body,
            from_email=self.sender.name_and_address,
            to=[self.mail_to],
            cc=None,
            reply_to=None,
            headers=self.mail_headers,
        )

        if self.file.name:
            msg.attach_file(self.local_file)

        # Send the email
        msg.send(fail_silently=fail_silently)
        self.replied = True
        self.replied_on = timezone.now()
        self.save()


class PostalMessageLinkClicked(Model):
    """
    https://docs.postalserver.io/developer/webhooks#message-click-event
    """

    class Meta(Model.Meta):
        verbose_name = "Postal: MessageLinkClicked"
        verbose_name_plural = "Postal: MessageLinkClicked"

    def save_from_payload(self, payload: dict):
        please_implement_save_from_payload("MessageLinkClicked", payload)


class PostalMessageLoaded(Model):
    """
    https://docs.postalserver.io/developer/webhooks#message-loadedopened-event
    """

    class Meta(Model.Meta):
        verbose_name = "Postal: Message Loaded"
        verbose_name_plural = "Postal: Messages Loaded"

    def save_from_payload(self, payload: dict):
        please_implement_save_from_payload("MessageLoaded", payload)


class PostalDomainDNSError(Model):
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
        verbose_name = "Postal: Domain DNS Error"
        verbose_name_plural = "Postal: Domain DNS Errors"

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
