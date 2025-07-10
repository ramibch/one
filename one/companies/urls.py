from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import CompanyDetailView, CompanyListView, JobDetailView, JobListView

urlpatterns = [
    path(_("job") + "/<int:pk>", JobDetailView.as_view(), name="job_detail"),
    path(_("jobs"), JobListView.as_view(), name="job_list"),
    path(_("list"), CompanyListView.as_view(), name="company_list"),
    path("<int:pk>", CompanyDetailView.as_view(), name="company_detail"),
]
