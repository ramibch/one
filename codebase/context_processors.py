from django.conf import settings

from .menus.models import FooterItem, FooterLink, NavbarLink, SocialMediaLink


def site_utilities(request):
    show_types = ["user" if request.user.is_authenticated else "no_user", "always"]
    return {
        "request": request,
        "website": settings.WEBSITE,
        "navbar_links": NavbarLink.objects.filter(show_type__in=show_types),
        "footer_items": FooterItem.objects.filter(show_type__in=show_types, footerlink__isnull=False),
        "footer_links": FooterLink.objects.filter(show_type__in=show_types, footer_item=None),
        "social_media_links": SocialMediaLink.objects.filter(show_type__in=show_types),
    }
