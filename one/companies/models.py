from auto_prefetch import ForeignKey, Model
from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _

from one.base.utils.choices import Genders
from one.base.utils.db import ChoiceArrayField


class ApplicationMethods(models.TextChoices):
    EMAIL = "email", _("Email")
    WEBSITE = "website", _("Own website")
    EXTERNAL = "external", _("External service")
    # Recluiter email?
    # JOBS_EMAILS ?
    # TODO: Update when


class Company(Model):
    name = models.CharField(max_length=128, unique=True)
    website = models.URLField(max_length=128)
    jobs_page_url = models.CharField(max_length=128, null=True, blank=True)
    jobs_page_html = models.TextField(null=True, blank=True)
    jobs_container_tag = models.CharField(default="div")
    jobs_container_class = models.CharField(max_length=256, null=True, blank=True)
    job_link_class = models.CharField(max_length=256, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    application_methods = ChoiceArrayField(
        models.CharField(max_length=32, choices=ApplicationMethods),
        default=list,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta(Model.Meta):
        verbose_name = _("company")
        verbose_name_plural = _("companies")


class CompanyLocation(Model):
    company = ForeignKey(Company, on_delete=models.CASCADE)
    geo_info = ForeignKey("geo.GoogleGeoInfo", on_delete=models.CASCADE)


class Person(Model):
    is_hr = models.BooleanField(default=False)
    company = ForeignKey(Company, on_delete=models.CASCADE)

    gender = models.CharField(max_length=64, choices=Genders, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    full_name = models.GeneratedField(
        expression=Concat("first_name", Value(" "), "last_name"),
        output_field=models.CharField(max_length=128),
        db_persist=True,
    )
    email = models.EmailField(max_length=64, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.full_name} ({self.company})"
