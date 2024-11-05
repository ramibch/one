from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from .menus.models import FooterItem, FooterLink, NavbarLink, SocialMediaLink


def site_utilities(request):
    show_types = ["user" if request.user.is_authenticated else "no_user", "always"]

    website = get_current_site(request).website

    return {
        "request": request,
        "website": website,
        "frontend": settings.FRONTEND,
        "navbar_links": NavbarLink.objects.filter(show_type__in=show_types, website=website),
        "footer_items": FooterItem.objects.filter(show_type__in=show_types, footerlink__isnull=False, website=website),
        "footer_links": FooterLink.objects.filter(show_type__in=show_types, footer_item=None, website=website),
        "social_media_links": SocialMediaLink.objects.filter(show_type__in=show_types, website=website),
    }
