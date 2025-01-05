from django.http import HttpRequest, HttpResponse

from ...clients.models import Client
from ...sites.models import Site


class PDFResponse(HttpResponse):
    def __init__(self, content, filename=None):
        super().__init__(content_type="application/pdf")
        self["Content-Disposition"] = f'filename="{filename}"'
        self.write(content)


class CustomHttpRequest(HttpRequest):
    client: Client
    site: Site
