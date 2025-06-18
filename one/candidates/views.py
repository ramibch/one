from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from one.candidates.forms import CandidateProfileForm, JobApplicationForm
from one.candidates.models import CandidateProfile, JobApplication


class ProfileListView(ListView):
    model = CandidateProfile
    template_name = "candidates/profile_list.html"


class PubProfileView(DetailView):
    model = CandidateProfile
    template_name = "candidates/profile_detail.html"
    queryset = CandidateProfile.objects.filter(is_public=True)


class ProfileView(LoginRequiredMixin, DetailView):
    model = CandidateProfile
    template_name = "candidates/profile_detail.html"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(user_id=self.request.user.id)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = "candidates/profile_edit.html"

    def get_object(self) -> type[CandidateProfile]:
        return get_object_or_404(
            self.model,
            pk=self.kwargs["pk"],
            user=self.request.user,
        )


class ProfileCreateView(LoginRequiredMixin, FormView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = "candidates/profile_create.html"


class JobApplicationView(FormView):
    model = JobApplication
    form_class = JobApplicationForm

    def form_valid(self, form: Any) -> HttpResponse:
        return super().form_valid(form)
