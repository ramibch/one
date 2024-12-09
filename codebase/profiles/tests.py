from django.urls import reverse

from config.test import TestCase


class ProfileUtilsTests(TestCase):
    def test_initial_profile_with_guest_user(self):
        response = self.client.get(reverse("profile_create"))
        request = response.wsgi_request
        self.assertTrue(hasattr(request, "session_obj"))
        self.assertEqual(response.status_code, 302)

    def test_initial_profile_with_logged_in_user(self):
        # https://stackoverflow.com/questions/9332541/django-get-user-logged-into-test-client
        pass
