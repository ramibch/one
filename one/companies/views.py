from typing import Any

from django import forms
from django.views.generic import DetailView

from one.candidates.models import TexCv

from .forms import ApplyForm
from .models import Company, Job


class JobDetailView(DetailView):
    model = Job

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        data = {"job": self.get_object()}
        ApplyForm.base_fields["cv"] = forms.ModelChoiceField(
            queryset=TexCv.objects.filter(
                profile__user_id=self.request.user.id,
            )
        )
        form = ApplyForm(initial=data)
        if form.fields["cv"].queryset.count() > 0:
            context["apply_form"] = form
        return context


class CompanyDetailView(DetailView):
    model = Company
