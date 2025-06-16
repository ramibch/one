from django import forms

from one.candidates.models import JobApplication


class ApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ("cv", "job")
        widgets = {"job": forms.HiddenInput()}
