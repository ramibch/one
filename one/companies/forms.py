from django import forms
from django.conf import settings

from one.candidates.models import JobApplication
from one.companies.models import Job


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ("job", "candidate", "language")
        widgets = {
            "job": forms.HiddenInput(),
            "candidate": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial = kwargs.get("initial") or {}
        candidate = initial.get("candidate")
        job = initial.get("job")

        if not candidate:
            return

        allowed_languages = candidate.get_languages()

        self.fields["language"].choices = [
            (code, name)
            for code, name in settings.LANGUAGES
            if code in allowed_languages
        ]

        if job:
            preferred = (
                job.language
                if job.language in allowed_languages
                else candidate.language
            )
            self.initial["language"] = preferred
        else:
            self.initial["language"] = candidate.language


class JobEditForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ("title", "body", "recruiter", "company_locations", "is_approved")
