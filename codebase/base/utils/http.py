from django.http import HttpRequest, HttpResponse

from ..models import ExtendedSite
from .middlewares import CountryDetails


class PDFResponse(HttpResponse):
    def __init__(self, content, filename=None):
        super().__init__(content_type="application/pdf")
        self["Content-Disposition"] = f'filename="{filename}"'
        self.write(content)


class CustomHttpRequest(HttpRequest):
    country: CountryDetails
    extendedsite: ExtendedSite
