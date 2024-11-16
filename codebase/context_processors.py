from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def site_utilities(request):
    show_types = ["user" if request.user.is_authenticated else "no_user", "always"]
    site = get_current_site(request)

    return {
        "request": request,
        "site": site,
        "frontend": settings.FRONTEND,
        "navbar_links": site.navbarlink_set.filter(show_type__in=show_types).distinct(),
        "footer_items": site.footeritem_set.filter(show_type__in=show_types, footerlink__isnull=False).distinct(),
        "footer_links": site.footerlink_set.filter(show_type__in=show_types, footer_item=None).distinct(),
        "social_media_links": site.socialmedialink_set.filter(show_type__in=show_types).distinct(),
    }
