from django import forms

from one.candidates.models import JobApplication


class ApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ("job", "candidate")
        widgets = {
            "job": forms.HiddenInput(),
            "candidate": forms.HiddenInput(),
        }
