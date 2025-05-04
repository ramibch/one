from django.contrib import admin, messages
from django.contrib.gis.admin import GISModelAdmin

from .models import GeoInfo, GoogleGeoInfo
from .tasks import update_google_geo_info_objects


@admin.register(GeoInfo)
class GeoInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "city", "postal_code", "latitude", "longitude")
    readonly_fields = tuple(field.name for field in GeoInfo._meta.fields)
    list_filter = ("is_in_european_union", "country_code", "time_zone")


@admin.register(GoogleGeoInfo)
class GoogleGeoInfoAdmin(GISModelAdmin):
    search_fields = ("address",)
    list_display = ("address", "latitude", "longitude")
    readonly_fields = ("payload", "latitude", "longitude")
    actions = ["update_attrs"]
    map_template = "admin/openlayers.html"
    openlayers_url = "https://openlayers.org/api/OpenLayers.js"

    @admin.action(description="📍 Update attrs from Google or payload")
    def update_attrs(modeladmin, request, queryset):
        count_max = 1000
        if queryset.count() > count_max:
            messages.warning(request, f"Too many objects. Limited at {count_max}")
        update_google_geo_info_objects(queryset[:count_max])
