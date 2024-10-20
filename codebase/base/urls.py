from django.urls import path

from .views import favicon, home, hx_seach_results, search

urlpatterns = [
    # search
    path("s/", search, name="search"),
    path("s/results/", hx_seach_results, name="search-results"),
    path("favicon.ico", favicon, name="favicon"),
    path("", home, name="home"),
]
