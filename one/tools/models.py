import os
import tempfile
from io import BytesIO
from subprocess import run

import qrcode
from barcode import generate
from barcode.writer import ImageWriter, SVGWriter
from django.core.files.base import ContentFile, File
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.template.loader import get_template
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

now = timezone.now()


class AbstractBarcode(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    png = models.ImageField(upload_to="barcodes", null=True)
    svg = models.ImageField(upload_to="barcodes", null=True)
    jpg = models.ImageField(upload_to="barcodes", null=True)

    def process(self):
        writers = {"png": ImageWriter, "jpg": ImageWriter, "svg": SVGWriter}
        format = self._meta.model.FORMAT
        for ext in writers:
            fp = BytesIO()
            path = f"{format}/{self.text}.{ext}"
            generate(format, self.text, writer=writers[ext](), output=fp)
            fp.seek(0)
            getattr(self, ext).save(path, ContentFile(fp.read()), save=True)

    def __str__(self):
        return self.text

    class Meta:
        abstract = True


class EAN14Barcode(AbstractBarcode):
    """digits = 13"""

    FORMAT = "ean14"
    text = models.CharField(
        max_length=13, validators=[MinLengthValidator(13), MaxLengthValidator(13)]
    )


class EAN13Barcode(AbstractBarcode):
    """digits = 12"""

    FORMAT = "ean13"
    text = models.CharField(
        max_length=12, validators=[MinLengthValidator(12), MaxLengthValidator(12)]
    )


class EAN13GuardBarcode(AbstractBarcode):
    """digits = 12"""

    FORMAT = "ean13-guard"
    text = models.CharField(
        max_length=12, validators=[MinLengthValidator(12), MaxLengthValidator(12)]
    )


class EAN8Barcode(AbstractBarcode):
    """digits = 7"""

    FORMAT = "ean8"
    text = models.CharField(
        max_length=7, validators=[MinLengthValidator(7), MaxLengthValidator(7)]
    )


class EAN8GuardBarcode(AbstractBarcode):
    """digits = 7"""

    FORMAT = "ean8-guard"
    text = models.CharField(
        max_length=7, validators=[MinLengthValidator(7), MaxLengthValidator(7)]
    )


class JANBarcode(AbstractBarcode):
    """digits = 12"""

    FORMAT = "jan"
    text = models.CharField(
        max_length=12, validators=[MinLengthValidator(12), MaxLengthValidator(12)]
    )


class CodabarBarcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "codabar"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class Code128Barcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "code128"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class Code39Barcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "code39"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class ISBN13Barcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "isbn13"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class GS1_128Barcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "gs1_128"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class ISBN10Barcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "isbn10"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class ISSNBarcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "issn"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class PZNBarcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "pzn"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class ITFBarcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "itf"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class UPCBarcode(AbstractBarcode):
    """
    TODO: Check digits and limits
    """

    FORMAT = "upc"
    text = models.CharField(
        max_length=32, validators=[MinLengthValidator(5), MaxLengthValidator(32)]
    )


class QRCode(models.Model):
    text = models.CharField(max_length=32)
    jpg = models.ImageField(upload_to="qcodes", null=True)

    def process(self):
        with tempfile.TemporaryFile() as tf:
            img = qrcode.make(self.text)
            img.save(tf)
            self.jpg.save(f"QR_{self.id}.jpg", File(tf), save=True)


class AbstractChart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=32, null=True)
    png = models.ImageField(upload_to="graphs", null=True)
    pdf = models.FileField(upload_to="graphs", null=True)
    svg = models.ImageField(upload_to="barcodes", null=True)
    source = models.TextField(null=True)

    def process(self):
        with tempfile.TemporaryDirectory() as tempdir:
            template = get_template(self.template_name)
            source = template.render({"self": self})
            with open(os.path.join(tempdir, "input.plt"), "x", encoding="utf-8") as f:
                f.write(source)
            for ext in ("png", "pdf", "svg"):
                output_file = f"output.{ext}"
                filepath = f"{self._meta.model_name}/{self.id}.{ext}"
                args = (
                    f'gnuplot -e "set terminal {ext}; '
                    f"set output '{output_file}'\" input.plt"
                )
                run(args, shell=True, capture_output=True, check=False, cwd=tempdir)
                with open(os.path.join(tempdir, output_file), "rb") as f:
                    filecontent = f.read()
                getattr(self, ext).save(filepath, ContentFile(filecontent), save=True)
            self.source = source
        self.save()

    class Meta:
        abstract = True


class SpiderChart(AbstractChart):
    template_name = "tools/gnuplot/spider.plt"
    labels = models.CharField(
        _("Labels in format: NameAxis1 NameAxis2 NameAxis3..."),
        null=True,
        max_length=128,
    )
    data = models.TextField(_("Data in format: Legend number1 number2 number3..."))
    fill = models.BooleanField(default=True)

    def render_labels(self):
        out = ""
        for count, label in enumerate(self.labels.split(), start=1):
            out += f"set paxis {count} label '{label}'\n"
        return mark_safe(out)

    def num(self):
        return len(self.labels.split())

    def num_plus_1(self):
        return self.num() + 1


class GanttChart(AbstractChart):
    template_name = "tools/gnuplot/gantt.plt"
    data = models.TextField(
        _("Data in format (dates as YYYY-MM-DD): TaskName DateStart DateEnd")
    )


class BarChart(AbstractChart):
    template_name = "tools/gnuplot/bar.plt"
    data = models.TextField(_("Data in format: ItemName ItemValue"))

    def render_data(self):
        out = ""
        for count, line in enumerate(self.data.splitlines(), start=0):
            out += f"{count} {line}\n"
        return mark_safe(out)


class HeatMapChart(AbstractChart):
    # Not used
    template_name = "tools/gnuplot/heatmap.plt"
    data = models.TextField(_("Matrix heat"))


class PointDataChart(AbstractChart):
    template_name = "tools/gnuplot/pointdata.plt"
    data = models.TextField(_("Data in format: X Y"))
    x_label = models.CharField(max_length=32, null=True)
    y_label = models.CharField(max_length=32, null=True)
