from django import forms

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


class SkillForm(forms.ModelForm):
    class Meta:
        model = CandidateSkill
        fields = ("name", "level")
        labels = {"name": "", "level": ""}
        # widgets = {"candidate": forms.HiddenInput()}


class EducationForm(forms.ModelForm):
    class Meta:
        model = CandidateEducation
        fields = ("institution_name", "title", "from_to", "description")
        labels = {"name": "", "level": ""}
