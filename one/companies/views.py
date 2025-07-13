from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, FormView, ListView

from .forms import ApplyForm
from .models import Company, Job


class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # data = {"job": self.get_object()}
        # ApplyForm.base_fields["cv"] = forms.ModelChoiceField(
        #     queryset=TexCv.objects.filter(
        #         candidate__user_id=self.request.user.id,
        #     )
        # )
        # form = ApplyForm(initial=data)
        # if form.fields["cv"].queryset.count() > 0:
        #     context["apply_form"] = form
        return context


class JobApplicationHxView(LoginRequiredMixin, FormView):
    form_class = ApplyForm
    template_name = "companies/partials/job_apply.html"
    ok_template_name = "companies/partials/job_applied.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        job = get_object_or_404(Job, pk=self.kwargs["pk"])
        candidate = getattr(request.user, "candidate", None)
        form = self.form_class(None, initial={"job": job, "candidate": candidate})
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


class JobListView(ListView):
    model = Job
    paginate_by = 100


class CompanyListView(ListView):
    model = Company
    paginate_by = 100


class CompanyDetailView(DetailView):
    model = Company
