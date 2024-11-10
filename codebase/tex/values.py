from django.utils.translation import gettext_lazy as _

LATEX_LANGUAGES = {"en": "english", "de": "german", "es": "spanish"}


TIPICAL_PAPERSIZES = {
    "a3paper": "A3 (297 mm x 420 mm)",
    "a4paper": "A4 (210 mm x 297 mm)",
    "a5paper": "A5 (148 mm x 210 mm)",
    "ansibpaper": "ANSI B (11 in. x 17 in.)",
    "letterpaper": "ANSI A (8.5 in. x 11 in.)",
    "legalpaper": "Legal (8.5 in. x 14 in.)",
}


PAGE_ORIENTATIONS = {
    "portrait": _("Portrait"),
    "landscape": _("Landscape"),
}


def get_margin(papersize):
    if papersize == "a3paper":
        return "2.5cm"
    elif papersize == "a4paper":
        return "2.0cm"
    elif papersize == "a5paper":
        return "1.5cm"
    elif papersize in "letterpaper,legalpaper":
        return "0.75in"
    elif papersize == "ansibpaper":
        return "1.00in"
