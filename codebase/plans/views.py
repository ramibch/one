from django.views.generic.list import ListView

from ..utils.generic_views import MultilinguageDetailView
from .models import Plan


class PlanDetailView(MultilinguageDetailView):
    model = Plan


class PlanListView(ListView):
    model = Plan
