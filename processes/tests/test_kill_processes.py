from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User


class TestKillProcessView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    @patch("processes.managers.ProcessManager.kill_process")
    def test_kill_process_view_success(self, mock_kill_process):
        self.client.login(username="testuser", password="testpass")
        pid = 1234
        response = self.client.post(reverse("processes:kill_process", args=[pid]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("processes:process_list"))
        mock_kill_process.assert_called_once_with(pid)
