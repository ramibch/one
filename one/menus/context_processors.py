from .models import ShowTypes


def menu_items(request) -> dict:
    show_types = [
        ShowTypes.USER if request.user.is_authenticated else ShowTypes.NO_USER,
        ShowTypes.ALWAYS,
    ]
    return {
        "request": request,
        "navbar_links": request.site.get_navbar_links(show_types),
        "footer_items": request.site.get_footer_items(show_types),
        "footer_links": request.site.get_footer_links(show_types),
        "social_media_links": request.site.get_social_media_links(show_types),
    }
