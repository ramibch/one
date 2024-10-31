from django.conf import settings

from .menus.models import MenuItem, PageLink, SocialMediaLink


def site_utilities(request):
    return {
        "request": request,
        "website": settings.WEBSITE,
        "navbar_items": MenuItem.objects.filter(show_in_navbar=True, pagelink__isnull=False),
        "navbar_links": PageLink.objects.filter(show_in_navbar=True, menu_item__isnull=True),
        "footer_items": MenuItem.objects.filter(show_in_footer=True, pagelink__isnull=False),
        "social_media_links": SocialMediaLink.objects.filter(show=True),

    }
