from copy import copy
from pathlib import Path

import auto_prefetch
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.text import slugify

from utils.files import write_local_file
from utils.telegram import report_to_admin


def upload_attachment(obj, filename):
    return f"emails/{slugify(obj.subject)}/{filename}"


class EmailTemplate(auto_prefetch.Model):
    subject = models.CharField(max_length=128)
    body = models.TextField()
    attachment1 = models.FileField(upload_to=upload_attachment, null=True, blank=True)
    attachment2 = models.FileField(upload_to=upload_attachment, null=True, blank=True)
    attachment3 = models.FileField(upload_to=upload_attachment, null=True, blank=True)
    reply_to = models.EmailField(max_length=64, null=True, blank=True)
    cc = models.EmailField(max_length=64, null=True, blank=True)
    var1_meaning = models.CharField(max_length=64, null=True, blank=True)
    var2_meaning = models.CharField(max_length=64, null=True, blank=True)
    var3_meaning = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.subject

    @cached_property
    def local_attachment1_path(self) -> Path:
        return write_local_file(self.attachment1.name)

    @cached_property
    def local_attachment2_path(self) -> Path:
        return write_local_file(self.attachment2.name)

    @cached_property
    def local_attachment3_path(self) -> Path:
        return write_local_file(self.attachment3.name)


class AbstractRecipient(auto_prefetch.Model):
    email_template = auto_prefetch.ForeignKey(
        EmailTemplate, on_delete=models.SET_NULL, null=True
    )
    address = models.EmailField(max_length=128)
    email_sent_on = models.DateTimeField(null=True, blank=True, editable=False)
    var1 = models.CharField(max_length=64, null=True, blank=True)
    var2 = models.CharField(max_length=64, null=True, blank=True)
    var3 = models.CharField(max_length=64, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    class Meta(auto_prefetch.Model.Meta):
        abstract = True

    @cached_property
    def admin_url(self):
        # the url to the Django admin form for the model instance
        info = (self._meta.app_label, self._meta.model_name)
        return reverse("admin:%s_%s_change" % info, args=(self.pk,))

    @cached_property
    def full_admin_url(self):
        return settings.WEBSITE_URL + self.admin_url

    def __str__(self) -> str:
        return self.address


class PastRecipient(AbstractRecipient):
    subject = models.CharField(max_length=128)
    body = models.TextField()


class Recipient(AbstractRecipient):
    draft = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False, editable=False)

    def text_replace(self, text: str):
        out = copy(text)
        vars = {"#var1": self.var1, "#var2": self.var2, "#var3": self.var3}
        for key, value in vars.items():
            if key in text:
                out = out.replace(key, value or key)
        return out

    def email_body(self):
        return self.text_replace(self.email_template.body)

    def email_subject(self):
        return self.text_replace(self.email_template.subject)

    def allow_to_send_email(self):
        return all(
            (
                "#var" not in self.email_body(),
                "#var" not in self.email_subject(),
                not self.draft,
                not self.email_sent,
            )
        )

    def send_email(self, delete_after=True):
        if not self.allow_to_send_email():
            reporting = "Not allowed to send Email\n\n"
            reporting += f"{self.full_admin_url}\n\n"
            reporting += f"{self.email_subject()}\n\n{self.email_body()}"
            report_to_admin(reporting)
            return

        reply_to = self.email_template.reply_to
        cc = self.email_template.cc
        none_or_reply_to = None if reply_to is None else [reply_to]
        none_or_cc = None if cc is None else [cc]
        message = EmailMessage(
            subject=self.email_subject(),
            body=self.email_body(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.address],
            cc=none_or_cc,
            reply_to=none_or_reply_to,
        )

        if self.email_template.local_attachment1_path:
            message.attach_file(self.email_template.local_attachment1_path)

        if self.email_template.local_attachment2_path:
            message.attach_file(self.email_template.local_attachment2_path)

        if self.email_template.local_attachment3_path:
            message.attach_file(self.email_template.local_attachment3_path)

        try:
            message.send(fail_silently=False)
        except Exception as e:
            report_to_admin(f"Error sending email:{e}\n\n{self.full_admin_url}")
            raise e

        PastRecipient.objects.create(
            email_template=self.email_template,
            address=self.address,
            subject=self.email_subject(),
            body=self.email_body(),
            email_sent_on=timezone.now(),
            var1=self.var1,
            var2=self.var2,
            var3=self.var3,
            remarks=self.remarks,
        )

        if delete_after:
            self.delete()
        else:
            self.email_sent = True
            self.email_sent_on = timezone.now()
            self.save()
