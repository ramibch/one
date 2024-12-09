from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_http_methods, require_POST
from django_htmx.http import HttpResponseClientRedirect
from django_minify_html.decorators import no_html_minification

from cvs.models import Cv
from tex.models import Tex

from . import forms as profile_forms
from .models import Profile


def hx_create_profile_cv(request, profile_id, tex_id, html_out):
    profile = get_object_or_404(Profile, id=profile_id)
    tex = get_object_or_404(Tex, id=tex_id)
    if tex.is_premium:
        if request.user.is_authenticated:
            if not request.user.plan.premium_templates:
                messages.warning(
                    request, _("This is a Premium template. Get a plan for using it.")
                )
                return HttpResponseClientRedirect(reverse_lazy("plan_list"))
        else:
            messages.warning(
                request, _("This is a Premium template. Get a plan for using it.")
            )
            return HttpResponseClientRedirect(reverse_lazy("plan_list"))

    cv, created = Cv.objects.get_or_create(profile=profile, tex=tex)
    if created:
        cv.tex.add_download()

    cv.render_files()
    context = {"cv": cv, "profile": profile}
    return render(request, f"profiles/cvs/{html_out}.html", context)


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.filter(user=request.user)
    else:
        profiles = Profile.objects.filter(session=request.session_obj)
    context = {"profiles": profiles}
    return render(request, "profiles/profile_list.html", context)


def profile_create(request: HttpRequest):
    profile = Profile(language_code=request.LANGUAGE_CODE)
    if request.user.is_authenticated:
        user = request.user
        if Profile.objects.filter(user=user).count() >= user.plan.profiles:
            messages.warning(
                request,
                _("You are not allowed to create another profile. Get a Premium Plan"),
            )
            return redirect("plan_list")
        profile.user = user
        profile.fullname = user.fullname
        profile.email = user.email
    else:
        if Profile.objects.filter(session=request.session_obj).count() >= 1:
            messages.info(request, _("Only one profile is allowed for guest users"))
            return redirect("profile_list")
        profile.category = "temporal"
        profile.session = request.session_obj
    profile.save()
    if request.htmx:
        return HttpResponseClientRedirect(profile.update_url())
    return HttpResponseRedirect(profile.update_url())


@no_html_minification
def profile_update(request, id):
    try:
        if request.user.is_authenticated and not request.user.is_staff:
            profile = Profile.objects.get(id=id, user=request.user)
        elif request.user.is_authenticated and request.user.is_staff:
            profile = Profile.objects.get(id=id)
        elif not request.user.is_authenticated:
            profile = Profile.objects.get(id=id, session=request.session_obj)
    except Profile.DoesNotExist:
        raise Http404

    context = profile.collect_context()
    return render(request, "profiles/profile_update.html", context)


@require_POST
def update_settings(request, klass, id):
    profile = get_object_or_404(Profile, id=id)
    Form = getattr(profile_forms, klass, None)
    if Form is None:
        return HttpResponseClientRedirect(profile.update_url())

    form = Form(request.POST, instance=profile)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(profile.update_url(params={"showSettings": "true"}))
    messages.warning(request, _("Error with profile settings"))
    context = profile.collect_context()
    context["showSettings"] = True
    return render(request, "profiles/profile_update.html", context)


@requires_csrf_token
@require_POST
def update_profile_fields(request, id):
    profile = get_object_or_404(Profile, id=id)
    for key in request.POST:
        setattr(profile, key, request.POST[key])
    profile.save()
    return HttpResponse(status=200)


def _render_new_child_formset(request, Model, Form, profile):
    new_formset = profile_forms.create_inlineformset(Form)(instance=profile)
    context = {
        "formset": new_formset,
        "update_url": profile.update_formset_url(Model),
        "order_url": profile.order_formset_url(Model),
    }
    return render(request, "profiles/partials/childset.html", context)


@require_POST
def update_child_formset(request, klass, id):
    profile = Profile.objects.get(id=id)
    Model, Form = profile_forms.get_child_model_and_form(klass)
    formset = profile_forms.create_inlineformset(Form)(request.POST, instance=profile)
    if formset.is_valid():
        formset.save()
    return _render_new_child_formset(request, Model, Form, profile)


@require_POST
def order_child_formset(request, klass, id):
    profile = Profile.objects.get(id=id)
    Model, Form = profile_forms.get_child_model_and_form(klass)
    formset = profile_forms.create_inlineformset(Form)(request.POST, instance=profile)
    if formset.is_valid():
        ids = [int(i) for i in request.POST.getlist("child-id")]
        for order, id in enumerate(ids, start=1):
            obj = formset.queryset.get(id=id)
            obj.order = order
            obj.save()
    return _render_new_child_formset(request, Model, Form, profile)


@require_http_methods(["DELETE"])
def delete_profile_child(request, klass, id):
    Model, Form = profile_forms.get_child_model_and_form(klass)
    child = get_object_or_404(Model, id=id)
    child.delete()
    return _render_new_child_formset(request, Model, Form, child.profile)


@require_POST
def profile_delete(request, id):
    object = get_object_or_404(Profile, id=id)
    object.delete()
    return HttpResponse(status=200)


@require_POST
def upload_profile_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    form = profile_forms.UploadPhotoForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
        saved_profile = form.save(commit=False)
        saved_profile.process_photo()

    context = {
        "cropphoto_form": profile_forms.CropPhotoForm(instance=saved_profile),
        "profile": profile,
    }
    return render(request, "profiles/photo/crop_form.html", context)


@require_POST
def crop_profile_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    form = profile_forms.CropPhotoForm(request.POST, instance=profile)
    if form.is_valid():
        saved_obj = form.save(commit=False)
        saved_obj.crop_photo()
    context = {"profile": profile}
    return render(request, "profiles/photo/cropped.html", context)


@require_http_methods(["DELETE"])
def delete_photo_files(request, id):
    profile = get_object_or_404(Profile, id=id)
    profile.full_photo.delete()
    profile.cropped_photo.delete()
    profile.crop_x, profile.crop_y = None, None
    profile.crop_height, profile.crop_width = None, None

    saved_profile = profile.save()
    context = {
        "uploadphoto_form": profile_forms.UploadPhotoForm(instance=saved_profile),
        "profile": saved_profile,
    }
    return render(request, "profiles/photo/new.html", context)
