from django.urls import path

from .views import (
    CompanyDetailView,
    CompanyListView,
    JobApplicationHxView,
    JobDetailView,
    JobEditHxView,
    JobListView,
)

urlpatterns = [
    # jobs
    path("jobs", JobListView.as_view(), name="job_list"),
    path("job/<uuid:pk>", JobDetailView.as_view(), name="job_detail"),
    path("job/<uuid:pk>/apply", JobApplicationHxView.as_view(), name="job_apply"),
    path("job/<uuid:pk>/edit", JobEditHxView.as_view(), name="job_edit"),
    # companies
    path("<int:pk>", CompanyDetailView.as_view(), name="company_detail"),
    path("", CompanyListView.as_view(), name="company_list"),
]
