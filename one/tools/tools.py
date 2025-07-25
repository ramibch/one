from functools import cache

from django.core.management.utils import get_random_secret_key
from django.forms import modelform_factory
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from . import models

# Texts
# TODO: These text must be defined somewhere else
# Create a Translatable Model ToolDetails or something
TEXT_GENERATE = _("Generate")

GENERAL_BARCODE_DESCRIPTION = _(
    "Generate your barcode with this online tool and "
    "download it for free in different formats"
)

# Keywords
GENERAL_KEYWORDS = _(
    "free, free online, free online tools, barcode generator, qr code, "
    "chart maker, hashing, engineering tools, maker, generator"
)
BARCODE_KEYWORDS = _(
    "free, barcode, barcodes, create, generate, generator, make, online, "
    "online barcode, barcodes online, barcode generator, "
    "online barcode generator, 2D code, QR code, barcode software"
)


# Templates
CHART_RESULTS_TEMPLATE = "tools/results/chart.html"
BARCODE_RESULTS_TEMPLATE = "tools/results/barcode.html"


class ToolListing:
    def __init__(self, title=None, description=None) -> None:
        self.title = title
        self.description = description if description is not None else title


TOOL_LISTING_OBJECT = ToolListing(
    title=_("Free Online Tools"),
    description=_("Generate charts, barcodes, QR codes with these free online tools"),
)


class Tool:
    def __init__(
        self,
        slug=None,
        title=None,
        form=None,
        process_func=None,
        body_md=None,
        category="general",
        html_cols=True,
        html_col1=6,
        index_listing=True,
        icon="🔨",
        process_text=TEXT_GENERATE,
        description=None,
        detail_template="tools/tool_detail.html",
        results_template="tools/results/general.html",
    ) -> None:
        self.slug = slug
        self.icon = icon
        self.form = form
        self.process_func = process_func
        self.title = title
        self.body_md = body_md
        self.index_listing = index_listing
        self.category = category
        self.html_cols = html_cols
        self.html_col1 = html_col1
        self.process_text = process_text
        self.detail_template = detail_template
        self.results_template = results_template
        self.description = description if description is not None else title

    @cached_property
    def url(self):
        return reverse_lazy("tool_detail", kwargs={"slug": self.slug})

    @cached_property
    def html_col2(self):
        return 12 - self.html_col1

    def __str__(self):
        return "Tool(" + self.icon + " " + self.slug + ")"


TOOLS = (
    Tool(
        icon="🔐",
        slug="md5",
        category="hashing",
        detail_template="tools/tool_md5.html",
        title=_("Online generator md5 hash of a string"),
    ),
    Tool(
        icon="🧾",
        slug="invoice",
        category="finance",
        detail_template="tools/tool_invoice.html",
        title=_("Online Invoice Generator"),
    ),
    Tool(
        slug="ean14",
        category="barcodes",
        title=_("Barcode Generator EAN14"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.EAN14Barcode, fields=["text"]),
    ),
    Tool(
        slug="ean13",
        category="barcodes",
        title=_("Barcode Generator EAN13"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.EAN13Barcode, fields=["text"]),
    ),
    Tool(
        slug="ean13-guards",
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        title=_("Barcode Generator EAN13 with guards"),
        form=modelform_factory(models.EAN13GuardBarcode, fields=["text"]),
        category="barcodes",
    ),
    Tool(
        slug="ean8",
        category="barcodes",
        title=_("Barcode Generator EAN8"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.EAN8Barcode, fields=["text"]),
    ),
    Tool(
        icon="🇯🇵",
        slug="jan",
        category="barcodes",
        title=_("Barcode Generator JAN"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.JANBarcode, fields=["text"]),
    ),
    Tool(
        slug="codabar",
        category="barcodes",
        title=_("Barcode Generator Codabar"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.CodabarBarcode, fields=["text"]),
    ),
    Tool(
        slug="code-128",
        category="barcodes",
        title=_("Barcode Generator Code 128"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.Code128Barcode, fields=["text"]),
    ),
    Tool(
        slug="code-39",
        category="barcodes",
        title=_("Barcode Generator Code 39"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.Code39Barcode, fields=["text"]),
    ),
    Tool(
        slug="isbn13",
        category="barcodes",
        title=_("Barcode Generator ISBN 13"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.ISBN13Barcode, fields=["text"]),
    ),
    Tool(
        slug="gs1-128",
        category="barcodes",
        #
        title=_("Barcode Generator GS1 128"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.GS1_128Barcode, fields=["text"]),
    ),
    Tool(
        slug="isbn10",
        category="barcodes",
        title=_("Barcode Generator ISBN 10"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.ISBN10Barcode, fields=["text"]),
    ),
    Tool(
        slug="issn",
        category="barcodes",
        title=_("Barcode Generator ISSN"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.ISSNBarcode, fields=["text"]),
    ),
    Tool(
        slug="pzn",
        category="barcodes",
        title=_("Barcode Generator PZN"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.PZNBarcode, fields=["text"]),
    ),
    Tool(
        slug="itf",
        category="barcodes",
        title=_("Barcode Generator ITF"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.ITFBarcode, fields=["text"]),
    ),
    Tool(
        slug="upc",
        category="barcodes",
        title=_("Barcode Generator UPC"),
        description=GENERAL_BARCODE_DESCRIPTION,
        results_template=BARCODE_RESULTS_TEMPLATE,
        form=modelform_factory(models.UPCBarcode, fields=["text"]),
    ),
    Tool(
        icon="📱",
        slug="qr-code",
        category="qrcodes",
        title=_("QR-Code Generator"),
        results_template="tools/results/qrcode.html",
        form=modelform_factory(models.QRCode, fields=["text"]),
    ),
    Tool(
        icon="🕸️",
        slug="spider",
        category="charts",
        title=_("Spider Chart Generator"),
        results_template=CHART_RESULTS_TEMPLATE,
        form=modelform_factory(models.SpiderChart, fields=["labels", "data", "fill"]),
    ),
    Tool(
        icon="🗓️",
        slug="gantt",
        category="charts",
        title=_("Gantt Chart Generator"),
        results_template=CHART_RESULTS_TEMPLATE,
        form=modelform_factory(models.GanttChart, fields=["title", "data"]),
    ),
    Tool(
        icon="📊",
        slug="bar",
        category="charts",
        title=_("Bar Chart Generator"),
        results_template=CHART_RESULTS_TEMPLATE,
        form=modelform_factory(models.BarChart, fields=["title", "data"]),
    ),
    Tool(
        icon="📈",
        slug="point-data",
        category="charts",
        title=_("Simple data Chart Generator"),
        results_template=CHART_RESULTS_TEMPLATE,
        form=modelform_factory(
            models.PointDataChart, fields=["title", "x_label", "y_label", "data"]
        ),
    ),
    Tool(
        icon="🔑",
        slug="django-secret-key",
        category="django",
        title=_("Django Secret Key Generator"),
        results_template="tools/results/dj_secret_key.html",
        process_func=get_random_secret_key,
        html_col1=4,
    ),
    Tool(
        icon="👨🏻‍💻",
        slug="postgres-db-for-django",
        category="django",
        title=_("Create PostgreSQL Database for a Django project"),
        detail_template="tools/tool_postgres.html",
    ),
)


@cache
def get_tool(slug):
    for tool in TOOLS:
        if tool.slug == slug:
            return tool


@cache
def get_related_tools(input_tool):
    return [
        tool
        for tool in TOOLS
        if input_tool.category == tool.category and input_tool.slug != tool.slug
    ]


@cache
def get_active_tools():
    return [tool for tool in TOOLS if tool.index_listing]
