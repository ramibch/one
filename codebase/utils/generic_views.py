import operator
from functools import reduce

from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView


class MultilinguageDetailView(DetailView):
    def get_object(self):
        params = {f"slug_{lang_code}": self.kwargs["slug"] for lang_code in settings.LANGUAGE_CODES}
        return get_object_or_404(self.model, reduce(operator.or_, (Q(**d) for d in [dict([i]) for i in params.items()])))
