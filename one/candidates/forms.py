from django import forms

from one.candidates.models import CandidateProfile, JobApplication


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ("cv", "job")


class CandidateProfileForm(forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ("first_name", "last_name")
