import uuid
from datetime import timedelta

from auto_prefetch import ForeignKey, Manager
from django.conf import settings
from django.db import models
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from langdetect import detect

from one.choices import Genders
from one.db import ChoiceArrayField, OneModel


class JobApplicationMethods(models.TextChoices):
    EMAIL = "email", _("Email")
    WEBSITE = "website", _("Own website")
    EXTERNAL = "external", _("External service")


class Company(OneModel):
    name = models.CharField(max_length=128, unique=True)
    website = models.URLField(max_length=128, null=True)
    remarks = models.TextField(blank=True, null=True)

    # Job related fields
    jobs_page_url = models.CharField(max_length=128, null=True, blank=True)
    jobs_page_html = models.TextField(null=True, blank=True, editable=False)
    jobs_scrape_ready = models.BooleanField(default=False)
    jobs_container_tag = models.CharField(default="div")
    jobs_container_class = models.CharField(max_length=256, null=True, blank=True)
    jobs_container_id = models.CharField(max_length=256, null=True, blank=True)
    job_link_class = models.CharField(max_length=256, null=True, blank=True)
    job_detail_container_tag = models.CharField(default="main")
    job_detail_container_class = models.CharField(max_length=256, null=True, blank=True)
    job_detail_container_id = models.CharField(max_length=256, null=True, blank=True)
    job_application_methods = ChoiceArrayField(
        models.CharField(max_length=32, choices=JobApplicationMethods),
        default=list,
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta(OneModel.Meta):
        verbose_name = _("company")
        verbose_name_plural = _("companies")

    @cached_property
    def jobs_page_html_is_empty(self):
        return self.jobs_page_html is None

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})

    @cached_property
    def url(self):
        return self.get_absolute_url()


class CompanyLocation(OneModel):
    local_name = models.CharField(max_length=128, blank=True, null=True)
    company = ForeignKey(Company, on_delete=models.CASCADE)
    geoinfo = ForeignKey("geo.GoogleGeoInfo", on_delete=models.CASCADE)

    def __str__(self):
        return self.geoinfo.address


class Person(OneModel):
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


class JobManager(Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True)


class Job(OneModel):
    id = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False,
    )
    language = models.CharField(max_length=8, choices=settings.LANGUAGES, default="de")
    title = models.CharField(max_length=128)
    body = models.TextField(blank=True, null=True)
    job_id = models.CharField(max_length=64, blank=True, null=True)

    source_url = models.URLField(max_length=256, blank=True, null=True)
    recruiter = ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=False,
    )
    company = ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=False,
    )
    company_locations = models.ManyToManyField(CompanyLocation, blank=True)
    duration = models.DurationField(default=timedelta(days=60))
    expires_on = models.DateTimeField(editable=False)
    is_active = models.BooleanField(default=True, editable=False)

    objects = JobManager()
    all_objects = Manager()

    class Meta(OneModel.Meta):
        indexes = [
            models.Index(
                name="job_company_fkey_idx",
                fields=["company"],
                condition=Q(company__isnull=False) & Q(is_active=True),
            ),
            models.Index(
                name="job_recruiter_fkey_idx",
                fields=["recruiter"],
                condition=Q(recruiter__isnull=False) & Q(is_active=True),
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.expires_on:
            base_time = self.created_at or now()
            self.expires_on = base_time + self.duration
        if self.body:
            self.language = detect(self.body)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})

    @cached_property
    def url(self):
        return self.get_absolute_url()

    @cached_property
    def apply_url(self):
        return reverse("candidate_job_apply", kwargs={"job_pk": self.pk})

    @cached_property
    def hx_apply_url(self):
        return reverse("job_apply", kwargs={"pk": self.pk})
