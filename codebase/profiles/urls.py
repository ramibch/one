from django.urls import path

from .views import (
    crop_profile_photo,
    delete_photo_files,
    delete_profile_child,
    hx_create_profile_cv,
    order_child_formset,
    profile_create,
    profile_delete,
    profile_list,
    profile_update,
    update_child_formset,
    update_profile_fields,
    update_settings,
    upload_profile_photo,
)

urlpatterns = [
    # profile list
    path("", profile_list, name="profile_list"),
    # create a profile (redirect)
    path("create/", profile_create, name="profile_create"),
    # profile update (edit view)
    path("<uuid:id>/", profile_update, name="profile_update"),
    # delete profile
    path("profile-delete/<uuid:id>/", profile_delete, name="profile_delete"),
    # delete child (obj from formset)
    path(
        "child-delete/<str:klass>/<int:id>/",
        delete_profile_child,
        name="profile_delete_child",
    ),
    # update child formset
    path(
        "formset/<str:klass>/<uuid:id>/",
        update_child_formset,
        name="profile_update_formset",
    ),
    # update profile field
    path(
        "profile-update-fields/<uuid:id>/",
        update_profile_fields,
        name="profile_update_fields",
    ),
    # update settings forms
    path(
        "profile-settings/<str:klass>/<uuid:id>/",
        update_settings,
        name="profile_update_settings",
    ),
    # order child formset
    path(
        "order/<str:klass>/<uuid:id>/",
        order_child_formset,
        name="profile_order_formset",
    ),
    # upload photo
    path(
        "upload-photo/<uuid:id>/",
        upload_profile_photo,
        name="profile_upload_photo",
    ),
    # crop photo
    path(
        "crop-photo/<uuid:id>/",
        crop_profile_photo,
        name="profile_crop_photo",
    ),
    # delete photos files
    path(
        "delete-photos/<uuid:id>/",
        delete_photo_files,
        name="profile_delete_photos",
    ),
    # create cv
    path(
        "create-cv/<uuid:profile_id>/<int:tex_id>/<str:html_out>/",
        hx_create_profile_cv,
        name="profile_create_cv",
    ),
]
