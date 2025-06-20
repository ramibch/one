from django.urls import path

from .views import (
    CandidateCreateView,
    CandidateEditView,
    CandidateListView,
    CandidateView,
    JobApplicationView,
    PubCandidateView,
    SkillEditHxView,
)

urlpatterns = [
    path("new", CandidateCreateView.as_view(), name="candidate_create"),
    path("<uuid:pk>", CandidateView.as_view(), name="candidate_detail"),
    path("<uuid:pk>/📝", CandidateEditView.as_view(), name="candidate_edit"),
    path("<uuid:pk>/hx/skills", SkillEditHxView.as_view(), name="candidateskills_edit"),
    path("<uuid:pk>/pub", PubCandidateView.as_view(), name="pub_candidate_detail"),
    # Profiles
    path("", CandidateListView.as_view(), name="candidate_list"),
    # Apps
    path("job-apply", JobApplicationView.as_view(), name="job_apply"),
]
