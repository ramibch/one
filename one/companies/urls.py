from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import CompanyDetailView, JobDetailView

urlpatterns = [
    path(_("job") + "/<int:pk>", JobDetailView.as_view(), name="job_detail"),
    path("<int:pk>", CompanyDetailView.as_view(), name="company_detail"),
]
