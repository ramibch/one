from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms import formset_factory
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from one.candidates.forms import CandidateForm, JobApplicationForm, SkillForm
from one.candidates.models import Candidate, CandidateSkill, JobApplication


class CandidateListView(ListView):
    model = Candidate
    template_name = "candidates/profile_list.html"


class PubCandidateView(DetailView):
    model = Candidate
    template_name = "candidates/profile_detail.html"
    queryset = Candidate.objects.filter(is_public=True)


class CandidateView(LoginRequiredMixin, DetailView):
    model = Candidate
    template_name = "candidates/profile_detail.html"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(user_id=self.request.user.id)


class CandidateEditView(LoginRequiredMixin, UpdateView):
    model = Candidate
    form_class = CandidateForm
    context_object_name = "profile"
    template_name = "candidates/profile_edit.html"
    hx_template_name = "candidates/partials/profile_form.html"

    def get_object(self) -> type[Candidate]:
        return get_object_or_404(
            self.model,
            pk=self.kwargs["pk"],
            user=self.request.user,
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Skills
        # qs_skills = self.object.candidateskill_set.all()
        SkillFormSet = formset_factory(SkillForm, extra=1)
        context["skill_formset"] = SkillFormSet()

        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.htmx:
            self.object = self.get_object()
            context = self.get_context_data(**kwargs)
            return render(request, self.hx_template_name, context)
        return super().post(request, *args, **kwargs)


class SkillEditHxView(LoginRequiredMixin, UpdateView):
    template_name = "candidates/partials/skill_formset.html"
    form_class = SkillForm
    model = CandidateSkill

    def get_queryset(self):
        return self.model.objects.filter(profile__user=self.request.user)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)


class CandidateCreateView(LoginRequiredMixin, FormView):
    model = Candidate
    form_class = CandidateForm
    template_name = "candidates/profile_create.html"


class JobApplicationView(FormView):
    model = JobApplication
    form_class = JobApplicationForm

    def form_valid(self, form: Any) -> HttpResponse:
        return super().form_valid(form)
