from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from one.candidates.models import CandidateProfile


class ProfileDetailView(DetailView):
    model = CandidateProfile
    template_name = "candidates/profile_detail.html"


class ProfileListView(ListView):
    model = CandidateProfile
    template_name = "candidates/profile_list.html"
