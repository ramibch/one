from .models import MenuListItem


def context(request):
    menu_items = MenuListItem.objects.all()
    return {
        "request": request,
        "navbar_list_items": menu_items.filter(show_in_navbar=True),
        "footer_list_items": menu_items,
    }
