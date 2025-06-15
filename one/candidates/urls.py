from django.urls import path

from .views import ProfileDetailView, ProfileListView

urlpatterns = [
    path("<uuid:pk>", ProfileDetailView.as_view(), name="candidateprofile_detail"),
    path("", ProfileListView.as_view(), name="candidateprofile_list"),
]
