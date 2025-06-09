from django.urls import path

from .views import SiteListView

urlpatterns = [
    path("", SiteListView.as_view(), name="site_list"),
]
