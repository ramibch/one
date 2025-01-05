from django.views.generic.list import ListView

from .models import FAQ


class FAQListView(ListView):
    model = FAQ
