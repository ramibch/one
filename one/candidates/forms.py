from django import forms
from django.utils.safestring import mark_safe

from one.candidates.models import (
    Candidate,
    CandidateEducation,
    CandidateSkill,
    JobApplication,
)


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ("cv", "job")


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = (
            "photo",
            "job_title",
            "first_name",
            "last_name",
            "email",
            "phone",
            "location",
            "linkedin_url",
            "website_url",
        )


class CandidateLabelsForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ("about_label", "skill_label", "education_label", "experience_label")


class SkillForm(forms.ModelForm):
    class Meta:
        model = CandidateSkill
        fields = ("name", "skill_type", "level")
        labels = {"name": "", "level": "", "skill_type": ""}


class EducationForm(forms.ModelForm):
    class Meta:
        model = CandidateEducation
        fields = (
            "title",
            "institution",
            "start_date",
            "end_date",
            "studying_now",
            "description",
        )
        widgets = {
            "start_date": forms.DateInput(attrs=dict(type="date")),
            "end_date": forms.DateInput(attrs={"type": "date", "x-model": "endDate"}),
            "studying_now": forms.CheckboxInput(attrs={"x-model": "studyingNow"}),
            "description": forms.Textarea(
                attrs={
                    "x-data": mark_safe(
                        "{ resize: () => { $el.style.height = '8px'; $el.style.height = $el.scrollHeight + 'px' } }"  # noqa: E501
                    ),
                    "x-init": "resize()",
                    "x-on:input": "resize()",
                }
            ),
        }
