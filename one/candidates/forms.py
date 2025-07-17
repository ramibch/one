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


class CandidateCreateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = (
            "language",
            "languages",
            "first_name",
            "last_name",
            "email",
            "phone",
        )
        widgets = {"languages": forms.CheckboxSelectMultiple()}


class CandidatePhotoEditForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ("photo",)


class CandidateEditForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = (
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


class CandidateExtraEditForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ("coverletter_body",)


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
            "end_date": forms.TextInput(
                attrs={
                    "type": "text",
                    "x-model": "endDate",
                    "x-bind:disabled": "studyingNow === true",
                }
            ),
            "studying_now": forms.CheckboxInput(
                attrs={
                    "x-model": "studyingNow",
                    "x-bind:disabled": "endDate !== ''",
                }
            ),
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
            "end_date": forms.TextInput(
                attrs={
                    "type": "text",
                    "x-model": "endDate",
                    "x-bind:disabled": "hereNow === true",
                }
            ),
            "here_now": forms.CheckboxInput(
                attrs={"x-model": "hereNow", "x-bind:disabled": "endDate !== ''"}
            ),
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
