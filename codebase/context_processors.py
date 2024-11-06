from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .utils.telegram import Bot
from .menus.models import FooterItem, FooterLink, NavbarLink, SocialMediaLink


def site_utilities(request):
    show_types = ["user" if request.user.is_authenticated else "no_user", "always"]
    site = get_current_site(request)
    website = getattr(site, "website", None)

    if website is None:
        Bot.to_admin(f"⚠️ The site {site.domain} has no Website associated!")

    return {
        "request": request,
        "website": website,
        "frontend": settings.FRONTEND,
        "navbar_links": NavbarLink.objects.filter(show_type__in=show_types, website=website),
        "footer_items": FooterItem.objects.filter(show_type__in=show_types, footerlink__isnull=False, website=website),
        "footer_links": FooterLink.objects.filter(show_type__in=show_types, footer_item=None, website=website),
        "social_media_links": SocialMediaLink.objects.filter(show_type__in=show_types, website=website),
    }
