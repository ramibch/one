from http import HTTPStatus
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import FormView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_htmx.http import reswap, retarget

from one.candidates.forms import (
    CandidateForm,
    EducationForm,
    JobApplicationForm,
    SkillForm,
)
from one.candidates.models import (
    Candidate,
    CandidateEducation,
    CandidateSkill,
    JobApplication,
)


def get_candidate_or_404(view, url_key="candidate_pk") -> type[Candidate] | Any:
    """util function to get a candidate object or 404"""
    return get_object_or_404(
        Candidate,
        pk=view.kwargs[url_key],
        user=view.request.user,
    )


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


@method_decorator(never_cache, name="dispatch")
class CandidateEditView(LoginRequiredMixin, UpdateView):
    model = Candidate
    form_class = CandidateForm
    context_object_name = "candidate"
    template_name = "candidates/profile_edit.html"
    hx_template_name = "candidates/partials/profile_form.html"

    def get_object(self) -> type[Candidate]:
        return get_candidate_or_404(self, url_key="pk")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Skills
        skill_qs = self.object.candidateskill_set.all()
        context["skill_edit_forms"] = [SkillForm(instance=sk) for sk in skill_qs]
        context["skill_new_form"] = SkillForm()
        # Education objects
        edu_qs = self.object.candidateeducation_set.all()
        context["education_edit_forms"] = [EducationForm(instance=e) for e in edu_qs]
        context["education_new_form"] = EducationForm()

        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.htmx:
            self.object = self.get_object()
            context = self.get_context_data(**kwargs)
            return render(request, self.hx_template_name, context)
        return super().post(request, *args, **kwargs)


class SkillCreateHxView(LoginRequiredMixin, CreateView):
    template_name = "candidates/partials/skill_edit_form.html"
    nok_template_name = "candidates/partials/skill_new_form.html"
    model = CandidateSkill
    form_class = SkillForm

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        candidate = get_candidate_or_404(self)
        context = {"candidate": candidate}
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.candidate = candidate
            self.object.save()
            context = context | self.get_context_data(kwargs=kwargs)
            context["skill_edit_form"] = self.form_class(instance=self.object)
            return render(request, self.template_name, context)
        else:
            context["skill_new_form"] = form
            response = render(request, self.nok_template_name, context)
            response = reswap(response, "outerHTML")
            return retarget(response, "#skill_new_form")


class SkillEditHxView(LoginRequiredMixin, UpdateView):
    template_name = "candidates/partials/skill_edit_form.html"
    form_class = SkillForm
    model = CandidateSkill

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        candidate = get_candidate_or_404(self)
        self.object = get_object_or_404(
            self.model,
            pk=self.kwargs["pk"],
            candidate=candidate,
        )
        form = self.form_class(request.POST, instance=self.object)
        context = {"candidate": candidate, "skill_edit_form": form}
        if form.is_valid():
            update_object = form.save(commit=False)
            update_object.candidate = candidate
            update_object.save()
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


class SkillOrderHxView(LoginRequiredMixin, TemplateView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        candidate = get_candidate_or_404(self)
        ids = [id_.strip() for id_ in request.POST.getlist("order") if id_.strip()]
        if not ids:
            return HttpResponseBadRequest("No skill IDs provided.")
        skills = CandidateSkill.objects.filter(candidate=candidate, id__in=ids)
        skill_map = {str(skill.id): skill for skill in skills}

        updated = []
        for order, skill_id in enumerate(ids, start=1):
            skill = skill_map.get(skill_id)
            if skill and skill.order != order:
                skill.order = order
                updated.append(skill)

        CandidateSkill.objects.bulk_update(updated, ["order"])
        return HttpResponse(status=HTTPStatus.OK)


class EducationCreateHxView(LoginRequiredMixin, CreateView):
    template_name = "candidates/partials/education_edit_form.html"
    nok_template_name = "candidates/partials/education_new_form.html"
    model = CandidateEducation
    form_class = EducationForm

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        candidate = get_candidate_or_404(self)
        context = {"candidate": candidate}
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.candidate = candidate
            self.object.save()
            context = context | self.get_context_data(kwargs=kwargs)
            context["education_edit_form"] = self.form_class(instance=self.object)
            return render(request, self.template_name, context)
        else:
            context["education_new_form"] = form
            response = render(request, self.nok_template_name, context)
            response = reswap(response, "outerHTML")
            return retarget(response, "#education_new_form")


class EducationDeleteHxView(LoginRequiredMixin, DeleteView):
    model = CandidateEducation

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


class EducationEditHxView(LoginRequiredMixin, UpdateView):
    template_name = "candidates/partials/skill_edit_form.html"
    form_class = EducationForm
    model = CandidateEducation

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        candidate = get_candidate_or_404(self)
        self.object = get_object_or_404(
            self.model,
            pk=self.kwargs["pk"],
            candidate=candidate,
        )
        form = self.form_class(request.POST, instance=self.object)
        context = {"candidate": candidate, "skill_edit_form": form}
        if form.is_valid():
            update_object = form.save(commit=False)
            update_object.candidate = candidate
            update_object.save()
            context = context | self.get_context_data(kwargs=kwargs)
        return render(request, self.template_name, context)


class EducationOrderHxView(LoginRequiredMixin, TemplateView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        candidate = get_candidate_or_404(self)
        ids = [id_.strip() for id_ in request.POST.getlist("order") if id_.strip()]
        if not ids:
            return HttpResponseBadRequest("No skill IDs provided.")
        edu_qs = CandidateEducation.objects.filter(candidate=candidate, id__in=ids)
        edu_map = {str(edu_obj.id): edu_obj for edu_obj in edu_qs}

        updated = []
        for order, edu_id in enumerate(ids, start=1):
            edu_obj = edu_map.get(edu_id)
            if edu_obj and edu_obj.order != order:
                edu_obj.order = order
                updated.append(edu_obj)

        CandidateEducation.objects.bulk_update(updated, ["order"])
        return HttpResponse(status=HTTPStatus.OK)


ExperienceCreateHxView = SkillCreateHxView
ExperienceDeleteHxView = SkillDeleteHxView
ExperienceEditHxView = SkillEditHxView
ExperienceOrderHxView = SkillOrderHxView
