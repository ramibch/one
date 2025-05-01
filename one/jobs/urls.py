from django.urls import path

from .views import apply_per_email, delete_profile

urlpatterns = [
    path("apply/<int:profile_id>/<int:job_id>", apply_per_email, name="job-apply"),
    path("profile-delete/<int:id>", delete_profile, name="profile-delete"),
]
