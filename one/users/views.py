from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django_htmx.http import HttpResponseClientRedirect

from .forms import CustomUserChangeForm


@login_required
def user_dashboard(request):
    return render(request, "users/dashboard.html")


@login_required
def edit_user(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, _("Account updated"))
        else:
            messages.error(request, _("An error occurred"))

    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "users/user_edit.html", context)


@login_required
def hx_delete_account(request):
    request.user.delete()
    messages.info(request, _("Account deleted"))
    return HttpResponseClientRedirect("/")
