from datetime import datetime
from io import BytesIO

import holidays
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.functional import cached_property
from pdf2image import convert_from_bytes
from PIL import Image

from one.base.utils.abstracts import TranslatableModel

from .compile import render_pdf
from .values import LATEX_LANGUAGES


class YearlyHolidayCalender(TranslatableModel):
    # https://holidays.readthedocs.io/en/latest/#
    year = models.SmallIntegerField()
    country = models.CharField(max_length=2, choices=settings.COUNTRIES)
    subdiv = models.CharField(max_length=128, null=True, blank=True)
    lang = models.CharField(max_length=2, choices=settings.LANGUAGES)
    pdf = models.FileField(null=True, blank=True, upload_to="calendars/")
    image = models.ImageField(null=True, blank=True, upload_to="calendars/")
    image1 = models.ImageField(null=True, blank=True, upload_to="calendars/")
    image2 = models.ImageField(null=True, blank=True, upload_to="calendars/")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.subdiv:
            return reverse_lazy(
                "tex_yearly_holiday_subdiv_calendar",
                args=(self.year, self.country, self.subdiv),
            )
        else:
            return reverse_lazy(
                "tex_yearly_holiday_no_subdiv_calendar",
                args=(self.year, self.country),
            )

    class Meta(TranslatableModel.Meta):
        unique_together = ("year", "country", "subdiv", "lang")

    @cached_property
    def title(self):
        extra = f" | {self.subdiv}" if self.subdiv else ""
        return f"{str(self.get_country_display())}{extra}"

    @cached_property
    def country_holidays(self):
        hdays = getattr(holidays, self.country)
        return hdays(subdiv=self.subdiv, years=self.year).items()

    def render(self):
        filename = f"{self.year}-{self.country}-{self.subdiv or ''}{self.lang}"

        with translation.override(self.lang):
            # country_holidays = getattr(holidays, self.country)
            holidays_part1, holidays_part2 = [], []

            for date, name in self.country_holidays:
                if date >= datetime(self.year, 7, 1).date():
                    holidays_part2.append((date, name))
                else:
                    holidays_part1.append((date, name))

            context = {
                "doc_language": LATEX_LANGUAGES[self.lang],
                "title": self.title,
                "year": self.year,
                "footer_url": "https://ramib.ch",
                "holidays_part1": holidays_part1,
                "holidays_part2": holidays_part2,
            }

            pdf_bytes = render_pdf("calendars/calendar.tex", context)
            self.pdf = ContentFile(pdf_bytes, name=f"{filename}.pdf")
            img1, img2 = convert_from_bytes(pdf_bytes)

        # image1 (page 1)
        img1_io = BytesIO()
        img1.save(img1_io, format="PNG")
        self.image1 = ContentFile(img1_io.getvalue(), name=f"{filename}_pag_1.png")

        # image2 (page 2)
        img2_io = BytesIO()
        img2.save(img2_io, format="PNG")
        self.image2 = ContentFile(img2_io.getvalue(), name=f"{filename}_pag_2.png")

        # image (page 1 + page 2)
        img = self.concatenate_images_vertically(img1, img2)
        img_io = BytesIO()
        img.save(img_io, format="PNG")
        self.image = ContentFile(img_io.getvalue(), name=f"{filename}.png")

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
