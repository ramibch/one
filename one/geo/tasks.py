import time

from huey import crontab
from huey.contrib import djhuey

from .models import GoogleGeoInfo


@djhuey.db_periodic_task(crontab(minute="34"))
def update_google_geo_info_objects(queryset=None):
    """
    Update Geo objects from Google.

    """
    queryset = queryset or GoogleGeoInfo.objects.filter(payload__isnull=True)

    for geo_obj in queryset:
        geo_obj.update_attrs()
        time.sleep(1)
