from django.conf import settings

from .models import FooterItem, NavbarItem


def site_utilities(request):
    return {
        "request": request,
        "settings": settings,
        "page_title": settings.WEBSITE_DEFAULT_PAGE_TITLE,
        "page_keywords": settings.WEBSITE_DEFAULT_PAGE_KEYWORDS,
        "navbar_items": NavbarItem.objects.all(),
        "footer_items": FooterItem.objects.all(),
    }
