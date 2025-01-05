from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from markdownx.widgets import AdminMarkdownxWidget

from .models import (
    Article,
    Feedback,
    Home,
    ListingProduct,
    ListingTag,
    MenuListItem,
    Page,
    PageLink,
    SearchTerm,
    Topic,
)

FORMFIELD_OVERRIDES_DICT = {
    models.TextField: {"widget": AdminMarkdownxWidget},
    models.ManyToManyField: {"widget": CheckboxSelectMultiple},
}


@admin.action(description="Make public")
def make_public(modeladmin, request, queryset):
    queryset.update(public=True)


@admin.action(description="Make not public")
def make_not_public(modeladmin, request, queryset):
    queryset.update(public=False)


@admin.action(description="Mark as promoted")
def mark_as_promoted(modeladmin, request, queryset):
    queryset.update(promoted=True)


@admin.action(description="Mark as not promoted")
def mark_as_not_promoted(modeladmin, request, queryset):
    queryset.update(promoted=False)


@admin.register(ListingProduct)
class ListingProductAdmin(admin.ModelAdmin):
    actions = (make_public, make_not_public, mark_as_promoted, mark_as_not_promoted)
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_filter = ("language", "promoted", "topics")
    list_display = ("dirname", "public", "promoted")
    readonly_fields = ("dirname", "image", "tags", "language")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    actions = (make_public, make_not_public)
    list_display = ("name", "public", "article_count", "slug")
    readonly_fields = ("name", "slug", "slug_en", "slug_de", "slug_es")
    list_filter = ("public",)


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ("title", "public")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_filter = ("public", "created_on", "language")
    list_display = ("title", "public", "anchor_tag")

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions["delete_selected"]
        return actions


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    formfield_overrides = FORMFIELD_OVERRIDES_DICT
    list_display = ("title", "public", "anchor_tag")

    def get_actions(self, request):
        actions = super().get_actions(request)
        del actions["delete_selected"]
        return actions


class PageLinkInline(admin.TabularInline):
    model = PageLink
    extra = 3


@admin.register(MenuListItem)
class MenuListItemAdmin(admin.ModelAdmin):
    inlines = (PageLinkInline,)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ("created_on",)
    list_display = ("__str__", "created_on")


@admin.register(ListingTag)
class ListingTagAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_es", "name_de")
    readonly_fields = ("name_en", "name_es", "name_de")


@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    pass
