from django.urls import path

from .views import edit_user, hx_delete_account, user_dashboard

urlpatterns = [
    path("", user_dashboard, name="user_dashboard"),
    path("edit/", edit_user, name="user-edit"),
    path("delete/", hx_delete_account, name="account_delete"),
]
