from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from utils.http import PDFResponse

from .compile import render_pdf

DOCUMENT_LANGUAGES = {"en": "english", "de": "german", "es": "spanish"}


class Holiday:
    def __init__(self, date, title) -> None:
        self.date = date
        self.title = title

    def tex_date(self):
        return self.date.strftime("%Y-%m-%d")


def test_calendar(request):
    if not settings.DEBUG:
        return HttpResponse("Unauthorized", status=401)
    lang_code = "es"
    year = 2024
    holidays_part1 = [
        Holiday(datetime(year, 1, 1), "Neujahr"),
        Holiday(datetime(year, 4, 3), "Testiing"),
    ]
    holidays_part2 = [Holiday(datetime(year, 12, 3), "Testing1!!")]

    context = {
        "doc_language": DOCUMENT_LANGUAGES[lang_code],
        "title": "My calendar title",
        "year": year,
        "footer_url": "https://ramiboutas.com",
        "holidays_part1": holidays_part1,
        "holidays_part2": holidays_part2,
    }
    pdf = render_pdf("calendar.tex", context)

    return PDFResponse(pdf, filename="calendar.pdf")
