from django.urls import path

from .views import (
    JobApplicationView,
    ProfileCreateView,
    ProfileListView,
    ProfileView,
    PubProfileView,
)

urlpatterns = [
    path("<uuid:pk>", ProfileView.as_view(), name="candidateprofile_detail"),
    path("<uuid:pk>/pub", PubProfileView.as_view(), name="pub_candidateprofile_detail"),
    path("new", ProfileCreateView.as_view(), name="candidateprofile_create"),
    path("", ProfileListView.as_view(), name="candidateprofile_list"),
    path("job-apply", JobApplicationView.as_view(), name="job_apply"),
]
