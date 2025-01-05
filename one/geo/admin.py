from django.contrib import admin

from .models import GeoInfo


@admin.register(GeoInfo)
class GeoInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "city", "postal_code", "latitude", "longitude")
    readonly_fields = tuple(field.name for field in GeoInfo._meta.fields)
    list_filter = ("is_in_european_union", "country_code", "time_zone")
