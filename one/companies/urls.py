from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    CompanyDetailView,
    CompanyListView,
    JobApplicationHxView,
    JobDetailView,
    JobListView,
)

urlpatterns = [
    # jobs
    path(_("jobs"), JobListView.as_view(), name="job_list"),
    path(_("job") + "/<uuid:pk>", JobDetailView.as_view(), name="job_detail"),
    path("job-apply/<uuid:pk>", JobApplicationHxView.as_view(), name="job_apply"),
    # companies
    path(_("list"), CompanyListView.as_view(), name="company_list"),
    path("<int:pk>", CompanyDetailView.as_view(), name="company_detail"),
]
