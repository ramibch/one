from django import forms
from django.utils.safestring import mark_safe

from one.candidates.models import (
    Candidate,
    CandidateEducation,
    CandidateExperience,
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
            "about",
        )


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
            "end_date": forms.TextInput(attrs={"type": "text", "x-model": "endDate"}),
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


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = CandidateExperience
        fields = (
            "job_title",
            "company_name",
            "start_date",
            "end_date",
            "here_now",
            "description",
        )
        widgets = {
            "end_date": forms.TextInput(attrs={"type": "text", "x-model": "endDate"}),
            "here_now": forms.CheckboxInput(attrs={"x-model": "hereNow"}),
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
