from django.views.generic import DetailView

from .models import Job


class JobDetailView(DetailView):
    model = Job
