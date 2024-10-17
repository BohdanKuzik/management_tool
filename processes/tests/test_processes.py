from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User


class TestProcessListView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    @patch("processes.managers.ProcessManager.get_processes")
    def test_process_list_view_with_authenticated_user(self, mock_get_processes):
        mock_get_processes.return_value = [
            {"pid": 1234, "status": "running", "name": "process1"},
            {"pid": 5678, "status": "stopped", "name": "process2"},
        ]

        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("processes:process_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "processes/process_list.html")
        self.assertContains(response, "process1")
        self.assertContains(response, "process2")
