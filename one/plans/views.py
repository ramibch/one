from django.views.generic.list import ListView

from .models import Plan


class PlanListView(ListView):
    model = Plan
