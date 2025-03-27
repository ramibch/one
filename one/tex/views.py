from django.http import Http404
from django.views.generic.detail import DetailView

from .models import YearlyHolidayCalender as Calendar


class YearlyHolidayCalenderView(DetailView):
    def get_object(self):
        year = self.kwargs.get("year")
        country = self.kwargs.get("country")
        subdiv = self.kwargs.get("subdiv")
        try:
            return Calendar.objects.exclude(pdf="", image="").get(
                year=year, country=country, subdiv=subdiv
            )
        except Calendar.DoesNotExist:
            raise Http404  # noqa: B904
