from django.urls import path

from .views import (
    CandidateCreateView,
    CandidateEditView,
    CandidateListView,
    CandidateView,
    JobApplicationView,
    PubCandidateView,
    SkillCreateHxView,
    SkillDeleteHxView,
    SkillEditHxView,
)

urlpatterns = [
    path(
        "new",
        CandidateCreateView.as_view(),
        name="candidate_create",
    ),
    path(
        "<uuid:pk>",
        CandidateView.as_view(),
        name="candidate_detail",
    ),
    path(
        "<uuid:pk>/edit",
        CandidateEditView.as_view(),
        name="candidate_edit",
    ),
    path(
        "<uuid:pk>/pub",
        PubCandidateView.as_view(),
        name="pub_candidate_detail",
    ),
    # Profiles
    path(
        "",
        CandidateListView.as_view(),
        name="candidate_list",
    ),
    # Apps
    path(
        "job-apply",
        JobApplicationView.as_view(),
        name="job_apply",
    ),
    # Skills
    path(
        "skill/<uuid:candidate_pk>/create",
        SkillCreateHxView.as_view(),
        name="candidateskill_create",
    ),
    path(
        "skill/<uuid:candidate_pk>/<uuid:pk>/delete",
        SkillDeleteHxView.as_view(),
        name="candidateskill_delete",
    ),
    path(
        "skill/<uuid:candidate_pk>/<uuid:pk>/edit",
        SkillEditHxView.as_view(),
        name="candidateskill_edit",
    ),
]
