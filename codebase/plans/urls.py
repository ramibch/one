from django.urls import path

from .views import PlanListView

urlpatterns = [
    path("<slug:slug>/", PlanListView.as_view(), name="plan_detail"),
    path("", PlanListView.as_view(), name="plan_list"),
]
