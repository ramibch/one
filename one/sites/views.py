from django.views.generic.list import ListView

from one.sites.models import Site


class SiteListView(ListView):
    queryset = Site.objects.filter(brand_name__isnull=False)
