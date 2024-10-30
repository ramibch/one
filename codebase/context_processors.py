from django.conf import settings

from .base.models import MenuItem, PageLink


def site_utilities(request):
    return {
        "request": request,
        "website": settings.WEBSITE,
        "navbar_items": MenuItem.objects.filter(show_in_navbar=True),
        "navbar_links": PageLink.objects.filter(show_in_navbar=True, menu_item__isnull=True),
        "footer_items": MenuItem.objects.filter(show_in_footer=True),
    }
