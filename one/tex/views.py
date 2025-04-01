from django.http import Http404
from django.shortcuts import render
from django.views.generic.detail import DetailView

from .models import YearlyHolidayCalender as YearlyHolidayCalender


class YearlyHolidayCalenderView(DetailView):
    def get_object(self):
        year = self.kwargs.get("year")
        country = self.kwargs.get("country")
        subdiv = self.kwargs.get("subdiv")
        try:
            return YearlyHolidayCalender.objects.exclude(pdf="", image="").get(
                year=year, country=country, subdiv=subdiv
            )
        except YearlyHolidayCalender.DoesNotExist:
            raise Http404  # noqa: B904


def temp_calendar(request, sd, c, y):
    c_dict = {
        "austria": "AT",
        "oesterreich": "AT",
        "germany": "DE",
        "deutschland": "DE",
        "alemania": "DE",
        "spain": "ES",
        "espana": "ES",
        "spanien": "ES",
        "suiza": "CH",
        "schweiz": "CH",
        "switzerland": "CH",
    }
    sd_dict = {
        # Germany
        "brandenburg": "BB",
        "berlin": "BE",
        "baden-wuerttemberg": "BW",
        "bayern": "BY",
        "bremen": "HB",
        "hessen": "HE",
        "hamburg": "HH",
        "mecklenburg-vorpommern": "MV",
        "niedersachsen": "NI",
        "nordrhein-westfalen": "NW",
        "rheinland-pfalz": "RP",
        "schleswig-holstein": "SH",
        "saarland": "SL",
        "sachsen": "SN",
        "sachsen-anhalt": "ST",
        "thueringen": "TH",
        # Austria
        "burgenland": "1",
        "Kaernten": "2",
        "niederoesterreich": "3",
        "oberoesterreich": "4",
        "salzburg": "5",
        "steiermark": "6",
        "tirol": "7",
        "vorarlberg": "8",
        "wien": "9",
        # Spain
        "andalucia": "AN",
        "aragon": "AR",
        "asturias": "AS",
        "vantabria": "CB",
        "vastilla-la-ancha": "CM",
        "castilla-y-leon": "CL",
        "cataluña": "CT",
        "extremadura": "EX",
        "galicia": "GA",
        "islas-baleares": "IB",
        "islas-canarias": "MC",
        "la-rioja": "RI",
        "madrid": "MD",
        "murcia": "MC",
        "navarra": "NC",
        "pais-vasco": "PV",
        "balencia": "VC",
    }

    country = c_dict.get(c)
    subdiv = sd_dict.get(sd)

    obj = YearlyHolidayCalender.objects.filter(
        year=y, country=country, subdiv=subdiv
    ).first()

    if obj:
        return render(request, "tex/yearlyholidaycalender_detail.html", {"object": obj})

    raise Http404
