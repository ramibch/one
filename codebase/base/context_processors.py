from django.conf import settings

from .models import MenuItem


def site_utilities(request):
    return {
        "request": request,
        "settings": settings,
        "page_title": settings.WEBSITE_DEFAULT_PAGE_TITLE,
        "page_keywords": settings.WEBSITE_DEFAULT_PAGE_KEYWORDS,
        "navbar_items": MenuItem.objects.filter(show_in_navbar=True),
        "footer_items": MenuItem.objects.filter(show_in_footer=True),
    }
