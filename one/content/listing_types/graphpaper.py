# https://www.agooddaytoprint.com/page/paper-size-chart-faq

# https://www.overleaf.com/learn/latex/Page_size_and_margins

# https://www.engineersupply.com/Drawing-Size-Reference-Table.aspx

# https://ctan.org/pkg/gridpapers

# https://www.etsy.com/de-en/listing/1336194162

# https://www.dadsworksheets.com/worksheets/graph-paper.html

from django.utils import translation
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from tex.values import PAGE_ORIENTATIONS, TIPICAL_PAPERSIZES, get_margin

from ..listings import Listing, validate_keywords, validate_tags

COLORS = {
    "std": _("Light blue"),
    "precocious": _("Light brown"),
    "ghostly": _("Gray"),
    "brickred": _("Brick color"),
    "engineer": _("Green"),
    "plumpad": _("Blue"),
}


PATTERNS = {
    "std": _("Quad paper"),  # Quadrille, ten squares per inch
    "majmin": _("Graph paper"),  # Graph paper, eight squares per inch
    "dot": _("Dot grid paper"),
    "hex": _("Hexagonal paper"),
    "hexup": _("Hexagonal paper rotated 90 degree"),
    "tri": _("Triangle grid"),
    "iso": _("Isometric grid"),
    "ruled": _("Ruled page"),
    "doubleruled": _("Double ruled page"),
}


LIST_OF_SQUARE_TAGS = [
    _("Squared paper"),
    _("Square graph"),
    _("Square grid"),
    _("Cartesian graph"),
]

LIST_OF_STD_TAGS = [
    _("Quadrille paper"),
    _("Quadrille"),
    _("Grid notes"),
] + LIST_OF_SQUARE_TAGS

LIST_OF_MAJMIN_TAGS = [
    _("Coordinate paper"),
    _("Engineering paper"),
    _("Engineering graph"),
    _("Architect paper"),
] + LIST_OF_SQUARE_TAGS

LIST_OF_HEX_TAGS = [
    _("Hexagon grid paper"),
    _("Hexagon paper"),
    _("Hexagon grid"),
    _("Hexagonal graph"),
    _("Chemistry paper"),
    _("Hex paper"),
    _("Hex map"),
    _("Hex board"),
    _("Hex grid"),
]

LIST_OF_TRI_TAGS = [
    _("Ternary plot"),
    _("Simplex plot"),
    _("Ternary graph"),
    _("De Finetti diagram"),
]

LIST_OF_DOT_TAGS = [_("Bullet journal"), _("Dotted paper"), _("Dots"), _("Dot Grid")]
LIST_OF_ISO_TAGS = [_("Isometric graph"), _("Isometric"), _("Iso"), _("Iso paper")]
LIST_OF_RULED_TAGS = [
    _("Line paper"),
    _("Ruled pages"),
    _("Lined paper"),
    _("Paper with lines"),
]


# do not repeat the words in PATTERNS
PATTERNS_EXTRA_TAGS = {
    "std": LIST_OF_STD_TAGS,
    "majmin": LIST_OF_MAJMIN_TAGS,
    "dot": LIST_OF_DOT_TAGS,
    "hex": LIST_OF_HEX_TAGS,
    "hexup": LIST_OF_HEX_TAGS,
    "tri": LIST_OF_TRI_TAGS,
    "iso": LIST_OF_ISO_TAGS,
    "ruled": LIST_OF_RULED_TAGS,
    "doubleruled": LIST_OF_RULED_TAGS,
}


def get_patternsizes(papersize: str, pattern_key: str) -> tuple:
    if papersize in "a3paper,a4paper,a5paper":
        if pattern_key in "std,dot,ruled,doubleruled":
            return ("2.0mm", "2.5mm", "3.7mm", "5.0mm", "10mm")
        elif pattern_key in "hex,hexup":
            return ("5.0mm", "10mm", "15mm", "20mm", "25mm")
        else:
            return ("2.0mm", "2.5mm", "5.0mm", "10mm")
    elif papersize in "ansibpaper,letterpaper,legalpaper":
        if pattern_key in "hex,hexup":
            return ("0.200in", "0.375in", "0.625in", "0.75in", "1.0in")
        else:
            return ("0.100in", "0.125in", "0.200in", "0.25in")


def get_tags(pattern_key: str):
    tags = PATTERNS_EXTRA_TAGS[pattern_key]
    if pattern_key in "std,dot,ruled,doubleruled":
        tags.append("Hobonichi")
    tags += [
        _("Grid paper"),
        _("Grid graph"),
        _("Digital Grid paper"),
        _("Digital Graph"),
        _("Printable Graph"),
    ]
    tags += list(PATTERNS.values())
    return validate_tags(tags)


def get_main_keywords(pattern_key):
    return str(PATTERNS[pattern_key])


def get_extra_keywords(pattern_key):
    """
    Examples (main + extra):
    - Digital Graph Paper | 24 Digital Notebook Paper Templates | Colored Graph Paper | Printable Paper for Note-Taking | 5 mm Grid | A4 & Letter
    - Printable Graph Paper | A4 & Letter | PDF, PNG | 3.7 mm, 5 mm, 1/4 inch, 10 mm square grid | planner inserts
    - 10 Squares per Inch Graph Paper | Printable | 10x10 Graph Paper | Cross Stitch Paper | A4 & Letter | Printable Grid Paper | Instant Download
    - Printable Graph Paper Bundle, 7 Different Templates, A4/A5/Letter/Half Size, Planner Inserts, Digital Notebook, Instant Download PDF
    - Printable Graph Paper | A4 & Letter | PDF, PNG | 3.7 mm, 5 mm, 1/4 inch, 10 mm square grid | planner inserts
    - Printable Graph Paper | Basic Notebook Paper | 5mm Grid | Notebook Pages | A4, A5, Letter | Digital PDF | Instant Download
    """
    return ", ".join(str(v) for v in PATTERNS_EXTRA_TAGS[pattern_key])


SUMMARY_INTRO = _(
    """Make your notes, drawings and your artistic pieces stand out with our digital graph paper bundle. You can customize your note-taking experience to suit your style with a variety of layout options, grid sizes, and colours to choose from."""
)

SUMMARY_USE = _(
    """Graph paper is indispensable for anyone seeking precision, organization, and visualization in their work or hobbies. Whether you are working on mathematics, engineering, art, or gaming, graph paper can help you bring your ideas to life with accuracy and clarity. With this graph paper you will be able to do the following:"""
)

SUMMARY_USE_GRAPH = _(
    """- Organize your thoughts by taking notes.
- Sketch geometric shapes with precision.
- Create your floorplans and architectural designs.
- Draw to-scale diagrams for buildings, bridges, and mechanical parts
- Plot experimental data points."""
)
SUMMARY_USE_DOT = _(
    """- Organize your tasks, goals, and schedules with flexibility and creativity.
- Create precise sketches and drawings effortlessly.
- Improve handwriting with dot grid paper's guidance.
- Create complex patterns with ease."""
)
SUMMARY_USE_TRI = _(
    """- Graph the relationships between three variables on an equilateral triangle.
- Plot the compositions of mixtures in chemistry, petrology, mineralogy and metallurgy.
- Create de Finetti diagrams to graph the genotype frequencies of populations.
- Use as a guide for precise designs and sketches."""
)
SUMMARY_USE_ISO = _(
    """- Easily create precise three-dimensional drawings.
- Visualize layouts and furniture arrangements with accuracy.
- Design immersive game levels and landscapes effortlessly.
- Explore three-dimensional concepts with clarity and depth.
- Achieve consistent perspective and depth in your artwork.
- Plan and design 3D models and sculptures with ease.
- Enhance spatial reasoning and problem-solving skills intuitively."""
)
SUMMARY_USE_HEX = _(
    """- Easily sketch and visualize organic molecules with precision.
- Design and create hex-based game boards effortlessly.
- Explore geometric shapes and patterns with precision.
- Draft maps with intricate terrain and land features.
- Create hexagon-based quilts, mosaics, and artwork with ease."""
)
SUMMARY_USE_RULED = _(
    """- Organize your thoughts by taking notes.
- Organize tasks, schedules, and project outlines clearly.
- Keep thoughts and reflections organized and legible.
- Use as a guide for precise designs and sketches."""
)

SUMMARY_LAYOUTS = _(
    """This product contains graph papers with different configurations: multiple paper sizes, two different page orientations (landscape/portrait), and two different margin configurations (with and without). Here is a list of the paper sizes supported by the product:"""
)

SUMMARY_PATTERN_SIZES = _(
    """Depending on the paper size standard, we offer different pattern sizes:"""
)

SUMMARY_COLORS = _(
    """Our graph papers come in a variety of grid colours! Choose the one (or the ones) that best suits your needs:"""
)


def get_summary(pattern_key):
    out = SUMMARY_INTRO.strip() + "\n\n"
    out += "⚡ " + _("USES AND APPLICATIONS") + "\n"
    out += SUMMARY_USE.strip() + "\n"
    if pattern_key in "std,majmin":
        out += SUMMARY_USE_GRAPH.strip()
    if pattern_key == "dot":
        out += SUMMARY_USE_DOT.strip()
    if pattern_key == "tri":
        out += SUMMARY_USE_TRI.strip()
    if pattern_key == "iso":
        out += SUMMARY_USE_ISO.strip()
    elif pattern_key in "hex,hexup":
        out += SUMMARY_USE_HEX.strip()
    elif pattern_key in "ruled,doubleruled":
        out += SUMMARY_USE_RULED.strip()
    out += "\n\n"
    # layouts
    out += "📄 " + _("LAYOUTS") + "\n"
    out += SUMMARY_LAYOUTS.strip() + "\n"
    out += "".join(f"- {i}\n" for i in TIPICAL_PAPERSIZES.values())
    out += "\n"
    out += "📐 " + _("PATTERN SIZES") + "\n"
    out += SUMMARY_PATTERN_SIZES.strip() + "\n"
    out += _("- ISO A Sizes") + ": "

    out += ", ".join(get_patternsizes("a4paper", pattern_key))
    out += "\n"
    out += _("- American ANSI Sizes") + ": "
    out += ", ".join(get_patternsizes("letterpaper", pattern_key))
    out += "\n\n"
    # colors
    out += "🎨 " + _("AVAILABLE COLORS") + "\n"
    out += SUMMARY_COLORS.strip() + "\n"
    out += "".join(f"- {i}\n" for i in COLORS.values())
    out += "\n"
    return out


def create_graphpaper(pattern_key) -> Listing:
    main_keywords = get_main_keywords(pattern_key)
    extra_keywords = get_extra_keywords(pattern_key)
    keywords = validate_keywords(f"{main_keywords}, {extra_keywords}")
    lang = translation.get_language()
    listing = Listing(
        keywords=keywords,
        title=main_keywords,
        tags=get_tags(pattern_key),
        dirname=slugify(main_keywords),
        listing_type="graphpaper",
        price=4.49,
        lang=lang,
    )
    listing.write_summary(get_summary(pattern_key))
    for fullpage in (False, True):
        margintext = _("without-margin") if fullpage else _("with-margin")
        for papersize, papersize_text in TIPICAL_PAPERSIZES.items():
            for colorset, colortext in COLORS.items():
                for patternsize in get_patternsizes(papersize, pattern_key):
                    for orientation, orientation_text in PAGE_ORIENTATIONS.items():
                        subfolders = (
                            f"{papersize_text} - {orientation_text}/{colortext}"
                        )
                        pdffilename = f"{patternsize}_{margintext}.pdf"
                        if (listing.files_path / subfolders / pdffilename).exists():
                            continue

                        context = {
                            "pattern": pattern_key,
                            "patternsize": patternsize,
                            "colorset": colorset,
                            "papersize": papersize,
                            "fullpage": fullpage,
                            "orientation": orientation,
                            "margin": get_margin(papersize),
                        }

                        listing.render_latex_file(
                            "graphpaper.tex",
                            pdffilename,
                            context,
                            images=False,
                            run_times=2,
                            subfolders=subfolders,
                        )
                        del context

    listing.zip_files(zipname=slugify(main_keywords))

    return listing
