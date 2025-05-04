from urllib.parse import urlencode

from auto_prefetch import ForeignKey, Model
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def upload_job_media(obj, filename):
    return f"jobs/{slugify(obj._meta.verbose_name_plural)}/{obj.id}/{filename}"


class Position(Model):
    name = models.CharField(max_length=64)
    position_type = models.CharField(max_length=16)
    remote = models.BooleanField(default=False)

    def __str__(self) -> str:
        emoji = "💻" if self.remote else "👨‍⚕️"
        return f"{emoji} {self.name} - {self.get_position_type_display()}"





class Job(Model):
    lang = models.CharField(max_length=8, choices=settings.LANGUAGES, default="de")
    title = models.CharField(max_length=64)

    recruiter = ForeignKey(Recruiter, on_delete=models.SET_NULL, null=True)
    position = ForeignKey(Position, on_delete=models.CASCADE, null=True)

    company_location = ForeignKey(
        "companies.CompanyLocation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        db_index=False,  # set in Meta
    )

    job_id = models.CharField(max_length=32, blank=True, null=True)
    source_url = models.URLField(max_length=128, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta(Model.Meta):
        indexes = [
            models.Index(
                name="job_company_location_fkey",
                fields=["company_location"],
                condition=models.Q(company_location__isnull=False),
            )
        ]

    def __str__(self) -> str:
        return self.title

    def email_apply_url(self, profile):
        return (
            WEBSITE_URL
            + reverse("job-apply", kwargs={"profile_id": profile.id, "job_id": self.id})
            + "?"
            + urlencode({"email": profile.email})
        )
