from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, FormView, ListView

from .forms import JobApplicationForm, JobEditForm
from .models import Company, Job


class SuperuserLoginRequiredMixin(LoginRequiredMixin):
    """Allows only superusers to access the view."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied  # or redirect to another page
        return super().dispatch(request, *args, **kwargs)


class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job


class JobApplicationHxView(LoginRequiredMixin, FormView):
    form_class = JobApplicationForm
    template_name = "companies/partials/job_apply.html"
    ok_template_name = "companies/partials/job_applied.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        job = get_object_or_404(Job, pk=self.kwargs["pk"])
        candidate = getattr(request.user, "candidate", None)
        initial = {"job": job, "candidate": candidate}
        form = self.form_class(None, initial=initial)
        context = {"apply_form": form, "job": job, "candidate": candidate}

        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.ok_template_name)

        job = get_object_or_404(Job, pk=self.kwargs["pk"])
        candidate = getattr(request.user, "candidate", None)
        context = {"apply_form": form, "job": job, "candidate": candidate}
        return render(request, self.template_name, context)


class JobEditHxView(SuperuserLoginRequiredMixin, FormView):
    form_class = JobEditForm
    template_name = "companies/partials/job_edit.html"

    def get_object(self):
        return get_object_or_404(Job, pk=self.kwargs["pk"])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        # You can add messages or other post-save logic here if needed
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        # On invalid form, just re-render with errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = self.get_object()
        return context


class JobListView(ListView):
    model = Job
    paginate_by = 12

    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .filter(body__isnull=False, is_approved=True, is_active=True)
            .exclude(body="")
        )


class CompanyListView(ListView):
    model = Company
    paginate_by = 100


class CompanyDetailView(DetailView):
    model = Company
