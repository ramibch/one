from django.urls import path

from .views import hx_seach_results, search

urlpatterns = [
    path("", search, name="search"),
    path("results/", hx_seach_results, name="search-results"),
]
