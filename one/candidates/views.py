from http import HTTPStatus
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import FormView, RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_htmx.http import reswap, retarget

from one.candidates.forms import (
    CandidateCreateForm,
    CandidateEditForm,
    CandidateExtraEditForm,
    EducationForm,
    ExperienceForm,
    JobApplicationForm,
    SkillForm,
)
from one.candidates.models import (
    Candidate,
    CandidateEducation,
    CandidateExperience,
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


class JobApplicationView(LoginRequiredMixin, FormView):
    model = JobApplication
    form_class = JobApplicationForm
    success_url = reverse_lazy("home")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # cxt["apply_form"] =
        # TODO:
        return super().get(request, *args, **kwargs)


class CandidateCreateOrEditRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str | None:
        candidate = getattr(self.request.user, "candidate", None)
        if candidate is None:
            return reverse("candidate_create")
        return candidate.edit_url


class CandidateDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "candidates/candidate_dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        candidate = getattr(self.request.user, "candidate", None)
        if candidate:
            context["candidate"] = candidate
            context["jobapps"] = JobApplication.objects.filter(candidate=candidate)
        return context


class CandidateCreateView(LoginRequiredMixin, FormView):
    model = Candidate
    form_class = CandidateCreateForm
    template_name = "candidates/candidate_create.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        candidate = getattr(self.request.user, "candidate", None)
        if candidate:
            return redirect(candidate.edit_url)
        initial = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
        }
        form = self.form_class(initial=initial)
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        context = {"form": form}
        if form.is_valid():
            obj = form.save(commit=False)
            # translation.activate(obj.language)
            obj.user = request.user
            obj.save()
            return redirect(obj.edit_url)

        return render(request, self.template_name, context)


class CandidateDeleteView(LoginRequiredMixin, DeleteView):
    model = Candidate
    success_url = reverse_lazy("home")

    def get_object(self) -> Any:
        return get_candidate_or_404(self, url_key="pk")


class JobApplicationDeleteHxView(LoginRequiredMixin, DeleteView):
    model = JobApplication

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.get_object().delete()
        return HttpResponse(status=HTTPStatus.OK)


class PubCandidateView(DetailView):
    model = Candidate
    template_name = "candidates/candidate_detail.html"
    queryset = Candidate.objects.filter(is_public=True)


class CandidateDetailView(LoginRequiredMixin, DetailView):
    context_object_name = "candidate"
    model = Candidate
    template_name = "candidates/candidate_detail.html"

    def get_queryset(self) -> QuerySet:
        return self.model.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["cvs"] = self.object.texcv_set.exclude(cv_image="")
        return context


@method_decorator(never_cache, name="dispatch")
class CandidateEditView(LoginRequiredMixin, TemplateView):
    model = Candidate
    form_class = CandidateEditForm
    template_name = "candidates/candidate_edit.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        candidate = get_candidate_or_404(self, url_key="pk")
        skill_qs = candidate.candidateskill_set.all()  # type: ignore
        edu_qs = candidate.candidateeducation_set.all()  # type: ignore
        exp_qs = candidate.candidateexperience_set.all()  # type: ignore
        context = {
            "candidate": candidate,
            "candidate_form": CandidateEditForm(instance=candidate),
            "candidate_extra_form": CandidateExtraEditForm(instance=candidate),
            "skill_edit_forms": [SkillForm(instance=sk) for sk in skill_qs],
            "skill_new_form": SkillForm(),
            "education_edit_forms": [EducationForm(instance=edu) for edu in edu_qs],
            "education_new_form": EducationForm(),
            "experience_edit_forms": [ExperienceForm(instance=exp) for exp in exp_qs],
            "experience_new_form": ExperienceForm(),
        }

        context = context | super().get_context_data(**kwargs)
        return render(request, self.template_name, context)


@method_decorator(never_cache, name="dispatch")
class CandidateEditHxView(LoginRequiredMixin, UpdateView):
    model = Candidate
    form_class = CandidateEditForm
    context_object_name = "candidate"
    template_name = "candidates/partials/candidate_form.html"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        form = self.form_class(request.POST, files=request.FILES, instance=self.object)
        if form.is_valid():
            form.save()
        context = {
            "candidate_form": form,
            "changed_data": form.changed_data,
        } | self.get_context_data(**kwargs)

        return render(request, self.template_name, context)


@method_decorator(never_cache, name="dispatch")
class CandidateExtraEditHxView(LoginRequiredMixin, UpdateView):
    model = Candidate
    form_class = CandidateExtraEditForm
    context_object_name = "candidate"
    template_name = "candidates/partials/candidate_extra_form.html"

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
        context = {
            "candidate_extra_form": form,
            "changed_data": form.changed_data,
        } | self.get_context_data(**kwargs)

        return render(request, self.template_name, context)


@method_decorator(never_cache, name="dispatch")
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


@method_decorator(never_cache, name="dispatch")
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
            context["section_saved"] = True
        return render(request, self.template_name, context)


@method_decorator(never_cache, name="dispatch")
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


@method_decorator(never_cache, name="dispatch")
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


@method_decorator(never_cache, name="dispatch")
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


@method_decorator(never_cache, name="dispatch")
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


@method_decorator(never_cache, name="dispatch")
class EducationEditHxView(LoginRequiredMixin, UpdateView):
    template_name = "candidates/partials/education_edit_form.html"
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
        context = {"candidate": candidate}
        if form.is_valid():
            update_object = form.save(commit=False)
            update_object.candidate = candidate
            update_object.save()
            context = context | self.get_context_data(kwargs=kwargs)
            context["section_saved"] = True
        context["education_edit_form"] = form
        return render(request, self.template_name, context)


@method_decorator(never_cache, name="dispatch")
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


@method_decorator(never_cache, name="dispatch")
class ExperienceCreateHxView(LoginRequiredMixin, CreateView):
    template_name = "candidates/partials/experience_edit_form.html"
    nok_template_name = "candidates/partials/experience_new_form.html"
    model = CandidateExperience
    form_class = ExperienceForm

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        candidate = get_candidate_or_404(self)
        context = {"candidate": candidate}
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.candidate = candidate
            self.object.save()
            context = context | self.get_context_data(kwargs=kwargs)
            context["experience_edit_form"] = self.form_class(instance=self.object)
            return render(request, self.template_name, context)
        else:
            context["experience_new_form"] = form
            response = render(request, self.nok_template_name, context)
            response = reswap(response, "outerHTML")
            return retarget(response, "#experience_new_form")


@method_decorator(never_cache, name="dispatch")
class ExperienceDeleteHxView(LoginRequiredMixin, DeleteView):
    model = CandidateExperience

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


@method_decorator(never_cache, name="dispatch")
class ExperienceEditHxView(LoginRequiredMixin, UpdateView):
    template_name = "candidates/partials/experience_edit_form.html"
    form_class = ExperienceForm
    model = CandidateExperience

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        candidate = get_candidate_or_404(self)
        self.object = get_object_or_404(
            self.model,
            pk=self.kwargs["pk"],
            candidate=candidate,
        )
        form = self.form_class(request.POST, instance=self.object)
        context = {"candidate": candidate}
        if form.is_valid():
            update_object = form.save(commit=False)
            update_object.candidate = candidate
            update_object.save()
            context = context | self.get_context_data(kwargs=kwargs)
            context["section_saved"] = True

        context["experience_edit_form"] = form
        return render(request, self.template_name, context)


@method_decorator(never_cache, name="dispatch")
class ExperienceOrderHxView(LoginRequiredMixin, TemplateView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        candidate = get_candidate_or_404(self)
        ids = [id_.strip() for id_ in request.POST.getlist("order") if id_.strip()]
        if not ids:
            return HttpResponseBadRequest("No skill IDs provided.")
        edu_qs = CandidateExperience.objects.filter(candidate=candidate, id__in=ids)
        edu_map = {str(edu_obj.id): edu_obj for edu_obj in edu_qs}

        updated = []
        for order, edu_id in enumerate(ids, start=1):
            edu_obj = edu_map.get(edu_id)
            if edu_obj and edu_obj.order != order:
                edu_obj.order = order
                updated.append(edu_obj)

        CandidateExperience.objects.bulk_update(updated, ["order"])
        return HttpResponse(status=HTTPStatus.OK)
