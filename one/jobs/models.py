from datetime import timedelta

from auto_prefetch import ForeignKey, Manager, Model
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.timezone import now


class JobManager(Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True)


class Job(Model):
    language = models.CharField(max_length=8, choices=settings.LANGUAGES, default="de")
    title = models.CharField(max_length=64)
    body = models.TextField()
    job_id = models.CharField(max_length=32, blank=True, null=True)
    source_url = models.URLField(max_length=128, blank=True, null=True)
    recruiter = ForeignKey(
        "companies.Person",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=False,  # Set in Meta
    )

    company_location = ForeignKey(
        "companies.CompanyLocation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_index=False,  # Set in Meta
    )
    duration = models.DurationField(default=timedelta(days=30))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    expires_on = models.DateTimeField(editable=False)
    is_active = models.BooleanField(default=True, editable=False)

    objects = JobManager()
    all_objects = Manager()

    class Meta(Model.Meta):
        indexes = [
            models.Index(
                name="job_company_location_fkey",
                fields=["company_location"],
                condition=Q(company_location__isnull=False) & Q(is_active=True),
            ),
            models.Index(
                name="job_recruiter_fkey",
                fields=["recruiter"],
                condition=Q(recruiter__isnull=False) & Q(is_active=True),
            ),
        ]

    def save(self, *args, **kwargs):
        if not self.expires_on:
            base_time = self.created_on or now()
            self.expires_on = base_time + self.duration
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
