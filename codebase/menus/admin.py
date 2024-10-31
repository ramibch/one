from django.contrib import admin
from django.db.migrations.recorder import MigrationRecorder
from django.utils.timezone import now

from .models import MenuItem, PageLink, SocialMediaLink



class PageLinkInline(admin.StackedInline):
    model = PageLink
    extra = 3

@admin.register(PageLink)
class PageLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "show_in_navbar", "order")
    list_filter = ("show_in_navbar", )

@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "show")
    list_filter = ("show", )


@admin.register(MenuItem)
class NavbarItemAdmin(admin.ModelAdmin):
    list_display = ("title", "show_in_navbar", "show_in_footer")
    list_filter = ("show_in_navbar", "show_in_footer")
    inlines = (PageLinkInline,)


