from django.views.generic import DetailView

from .models import Company, Job


class JobDetailView(DetailView):
    model = Job


class CompanyDetailView(DetailView):
    model = Company
