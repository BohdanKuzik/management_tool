from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestIndexView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_index_view_with_authenticated_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("processes:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "processes/process_list.html")

    def test_index_view_with_anonymous_user(self):
        response = self.client.get(reverse("processes:index"))
        self.assertEqual(response.status_code, 302)
        login_url = reverse("processes:login") + "?next=" + reverse("processes:index")
        self.assertRedirects(response, login_url)
