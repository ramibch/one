from datetime import datetime
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from pdf2image import convert_from_bytes
from PIL import Image

from one.base.utils.abstracts import TranslatableModel

from .compile import render_pdf
from .values import LATEX_LANGUAGES


class TexHoliday:
    def __init__(self, date, title) -> None:
        self.date = date
        self.title = title

    def tex_date(self):
        return self.date.strftime("%Y-%m-%d")


class YearlyHolidayCalender(TranslatableModel):
    # https://holidays.readthedocs.io/en/latest/#
    year = models.SmallIntegerField()
    title = models.CharField(max_length=256)
    pdf = models.FileField(null=True, blank=True)
    image1 = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

    def render(self):
        lang_code = "es"

        holidays_part1 = [
            TexHoliday(datetime(self.year, 1, 1), "Neujahr"),
            TexHoliday(datetime(self.year, 4, 3), "Testiing"),
        ]
        holidays_part2 = [TexHoliday(datetime(self.year, 12, 3), "Testing1!!")]

        context = {
            "doc_language": LATEX_LANGUAGES[lang_code],
            "title": "My calendar title",
            "year": self.year,
            "footer_url": "https://ramiboutas.com",
            "holidays_part1": holidays_part1,
            "holidays_part2": holidays_part2,
        }

        pdf_bytes = render_pdf("calendars/calendar.tex", context)
        self.pdf = ContentFile(pdf_bytes, name="test-calendar.pdf")
        img1, img2 = convert_from_bytes(pdf_bytes)

        # image1 (page 1)
        img1_io = BytesIO()
        img1.save(img1_io, format="PNG")
        self.image1 = ContentFile(img1_io.getvalue(), name="pag_1.png")

        # image2 (page 2)
        img2_io = BytesIO()
        img2.save(img2_io, format="PNG")
        self.image2 = ContentFile(img2_io.getvalue(), name="pag_2.png")

        # image (page 1 + page 2)
        img = self.concatenate_images_vertically(img1, img2)
        img_io = BytesIO()
        img.save(img_io, format="PNG")
        self.image = ContentFile(img_io.getvalue(), name="calendar.png")

        self.save()

    def concatenate_images_vertically(self, img1, img2):
        """Concatenates two PIL images vertically."""
        # Get dimensions
        width1, height1 = img1.size
        width2, height2 = img2.size

        # Width as max of both and height as the sum
        new_width = max(width1, width2)
        new_height = height1 + height2

        # Blank image with white background
        new_img = Image.new("RGB", (new_width, new_height), color=(255, 255, 255))

        # Paste both images
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (0, height1))

        return new_img
