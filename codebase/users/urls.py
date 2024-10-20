from django.urls import path

from .views import edit_user, hx_delete_user, user_dashboard

urlpatterns = [
    path("", user_dashboard, name="user-dashboard"),
    path("edit/", edit_user, name="user-edit"),
    path("delete/<int:id>/", hx_delete_user, name="user-delete"),
    # path("<int:id>/password/", redirect_change_password),
]
