from django.views.generic.detail import DetailView

from .models import Page


class PageDetailView(DetailView):
    model = Page
