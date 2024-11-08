from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from .menus.models import FooterItem, FooterLink, NavbarLink, SocialMediaLink
from django.contrib.sites.models import Site

def site_utilities(request):
    show_types = ["user" if request.user.is_authenticated else "no_user", "always"]
    site = get_current_site(request)


    site = Site.objects.select_related("navbarlink_set", "footeritem_set", "footerlink_set", "socialmedialink_set").get(domain=request.get_host())


    return {
        "request": request,
        "site": site,
        "frontend": settings.FRONTEND,
        "navbar_links": site.navbarlink_set.filter(show_type__in=show_types),
        "footer_items": site.footeritem_set.filter(show_type__in=show_types, footerlink__isnull=False),
        "footer_links": site.footerlink_set.filter(show_type__in=show_types, footer_item=None),
        "social_media_links": site.socialmedialink_set.filter(show_type__in=show_types),
        # "navbar_links": NavbarLink.objects.filter(show_type__in=show_types, site=site),
        # "footer_items": FooterItem.objects.filter(show_type__in=show_types, footerlink__isnull=False, site=site),
        # "footer_links": FooterLink.objects.filter(show_type__in=show_types, footer_item=None, site=site),
        # "social_media_links": SocialMediaLink.objects.filter(show_type__in=show_types, site=site),
    }
