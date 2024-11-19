from django.contrib.sites.shortcuts import get_current_site


def site_utilities(request):
    show_types = ["user" if request.user.is_authenticated else "no_user", "always"]
    site = get_current_site(request)

    return {
        "request": request,
        "site": site,
        "navbar_links": site.extendedsite.get_navbar_links(show_types),
        "footer_items": site.extendedsite.get_footer_items(show_types),
        "footer_links": site.extendedsite.get_footer_links(show_types),
        "social_media_links": site.extendedsite.get_social_media_links(show_types),
    }
