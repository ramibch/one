from django.http import HttpResponse


class PDFResponse(HttpResponse):
    def __init__(self, content, filename=None):
        super().__init__(content_type="application/pdf")
        self["Content-Disposition"] = f'filename="{filename}"'
        self.write(content)
