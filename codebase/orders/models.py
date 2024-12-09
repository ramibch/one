import uuid

import auto_prefetch
from django.conf import settings
from django.core.mail import EmailMessage
from django.db import models
from django.urls import reverse
from django.utils import timezone, translation
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from content.models import ListingProduct

EMAIL_BODY = _("""Thank you very much for your purchase. Attached you will find your order.

Remember that if you have any questions, you can contact me directly to this email!

Best wishes!
Rami
""")


class Customer(auto_prefetch.Model):
    name = models.CharField(max_length=512, default="", blank=True, null=True)
    email = models.CharField(max_length=512, default="", blank=True, null=True)
    address_city = models.CharField(max_length=512, default="", blank=True, null=True)
    address_country = models.CharField(
        max_length=512, default="", blank=True, null=True
    )
    address_line1 = models.CharField(max_length=512, default="", blank=True, null=True)
    address_line2 = models.CharField(max_length=512, default="", blank=True, null=True)
    address_postal_code = models.CharField(
        max_length=512, default="", blank=True, null=True
    )
    address_state = models.CharField(max_length=512, default="", blank=True, null=True)

    def __str__(self):
        return f"Customer({self.id} - {self.name} - {self.email})"


class ProductOrder(auto_prefetch.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    event_id = models.CharField(max_length=512, default="", blank=True)
    invoice_id = models.CharField(max_length=512, default="", blank=True)
    invoice_pdf = models.CharField(max_length=2048, null=True, blank=True)
    invoice_payload = models.TextField(null=True)
    payment_intent = models.CharField(max_length=512, default="", blank=True)
    checkout_payload = models.TextField(null=True)
    product = models.ForeignKey(ListingProduct, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)

    def has_expired(self):
        return timezone.now() - self.created_on > timezone.timedelta(days=2)

    @cached_property
    def email_subject(self):
        return self.product.title

    @cached_property
    def email_hello(self):
        return f"Hey {self.customer.name}!"

    def get_email_body(self):
        return self.email_hello + "\n\n" + EMAIL_BODY

    def send_email(self):
        try:
            translation.activate(self.product.language)
        except Exception:
            translation.activate("en")

        message = EmailMessage(
            self.email_subject,
            self.get_email_body(),
            settings.DEFAULT_FROM_EMAIL,
            [self.customer.email],
        )

        for filepath in self.product.get_listing().files_path.iterdir():
            message.attach_file(filepath)

        message.send(fail_silently=False)

    @cached_property
    def success_checkout_url(self):
        return reverse("order-detail", kwargs={"uuid": self.uuid})

    @cached_property
    def cancel_checkout_url(self):
        return self.product.page_url

    @cached_property
    def invoice_pdf_url(self):
        return reverse("order-invoice", kwargs={"uuid": self.uuid})

    def __str__(self):
        return f"ProductOrder({self.id} - {self.product.dirname})"
