from .http import CustomHttpRequest


def site_utilities(request: CustomHttpRequest) -> dict:
    show_types = ["user" if request.user.is_authenticated else "no_user", "always"]
    return {
        "request": request,
        "navbar_links": request.site.get_navbar_links(show_types),
        "footer_items": request.site.get_footer_items(show_types),
        "footer_links": request.site.get_footer_links(show_types),
        "social_media_links": request.site.get_social_media_links(show_types),
    }
