from django.urls import path

from .views import tool_detail, tool_index

urlpatterns = [
    path("", tool_index, name="tool_list"),
    path("<str:slug>/", tool_detail, name="tool_detail"),
]
