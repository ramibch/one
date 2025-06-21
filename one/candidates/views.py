from http import HTTPStatus
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_htmx.http import retarget

from one.candidates.forms import CandidateForm, JobApplicationForm, SkillForm
from one.candidates.models import Candidate, CandidateSkill, JobApplication


class JobApplicationView(FormView):
    model = JobApplication
    form_class = JobApplicationForm

    def form_valid(self, form: Any) -> HttpResponse:
        return super().form_valid(form)


class CandidateListView(ListView):
    model = Candidate
    template_name = "candidates/profile_list.html"


class CandidateCreateView(LoginRequiredMixin, FormView):
    model = Candidate
    form_class = CandidateForm
    template_name = "candidates/profile_create.html"


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
    context_object_name = "candidate"
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
        qs_skills = self.object.candidateskill_set.all()
        skill_forms = []
        for skill in qs_skills:
            skill_forms.append(SkillForm(instance=skill))

        context["skill_edit_forms"] = skill_forms
        context["skill_new_form"] = SkillForm()
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.htmx:
            self.object = self.get_object()
            context = self.get_context_data(**kwargs)
            return render(request, self.hx_template_name, context)
        return super().post(request, *args, **kwargs)


class SkillCreateHxView(LoginRequiredMixin, CreateView):
    template_name = "candidates/partials/skills_edit.html"
    nok_template_name = "candidates/partials/skill_form_new.html"
    model = CandidateSkill
    form_class = SkillForm

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)  # type: ignore
        candidate = get_object_or_404(
            Candidate,
            pk=self.kwargs["candidate_pk"],
            user=self.request.user,
        )
        context = {"candidate": candidate}
        if form.is_valid():
            skill = form.save(commit=False)
            skill.candidate = candidate
            skill.save()
            self.object = skill
            context = context | self.get_context_data(kwargs=kwargs)
            qs = candidate.candidateskill_set.all()
            context["skill_edit_forms"] = [SkillForm(instance=skill) for skill in qs]
            context["skill_new_form"] = SkillForm()
            return render(request, self.template_name, context)
        else:
            context["skill_new_form"] = form
            resp = render(request, self.nok_template_name, context)
            return retarget(resp, "#skill_form_new")


class SkillEditHxView(LoginRequiredMixin, UpdateView):
    template_name = "candidates/partials/skill_form_edit.html"
    form_class = SkillForm
    model = CandidateSkill

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)  # type: ignore
        candidate = get_object_or_404(
            Candidate,
            pk=self.kwargs["candidate_pk"],
            user=self.request.user,
        )
        context = {"candidate": candidate, "skill_edit_form": form}
        if form.is_valid():
            skill = form.save(commit=False)
            skill.candidate = candidate
            skill.save()
            self.object = skill
            context = context | self.get_context_data(kwargs=kwargs)
        return render(request, self.template_name, context)


class SkillDeleteHxView(LoginRequiredMixin, DeleteView):
    model = CandidateSkill

    def get_object(self) -> Any:
        return get_object_or_404(
            self.model,
            candidate__pk=self.kwargs["candidate_pk"],
            candidate__user=self.request.user,
            pk=self.kwargs["pk"],
        )

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(status=HTTPStatus.OK)
