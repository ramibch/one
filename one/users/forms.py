from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import get_language


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        user.sites.add(request.site)
        user.language = get_language()
        user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name")
