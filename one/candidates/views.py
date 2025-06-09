from django.views.generic.detail import DetailView

from one.candidates.models import CandidateProfile


class ProfileDetailView(DetailView):
    model = CandidateProfile
    template_name = "candidates/profile_detail.html"
