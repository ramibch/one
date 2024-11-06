from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from .menus.models import FooterItem, FooterLink, NavbarLink, SocialMediaLink


def site_utilities(request):
    show_types = ["user" if request.user.is_authenticated else "no_user", "always"]
    site = get_current_site(request)

    return {
        "request": request,
        "site": site,
        "frontend": settings.FRONTEND,
        "navbar_links": NavbarLink.objects.filter(show_type__in=show_types, site=site),
        "footer_items": FooterItem.objects.filter(show_type__in=show_types, footerlink__isnull=False, site=site),
        "footer_links": FooterLink.objects.filter(show_type__in=show_types, footer_item=None, site=site),
        "social_media_links": SocialMediaLink.objects.filter(show_type__in=show_types, site=site),
    }
