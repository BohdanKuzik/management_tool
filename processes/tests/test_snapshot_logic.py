import json

from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User

from processes.models import Snapshot


class TestTakeSnapshotView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    @patch("processes.managers.ProcessManager.get_processes")
    @patch("processes.managers.SnapshotManager.create_snapshot")
    def test_take_snapshot_view_success(self, mock_create_snapshot, mock_get_processes):
        mock_get_processes.return_value = [{"pid": 1234, "status": "running"}]

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("processes:take_snapshot"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("processes:process_list"))

        self.assertEqual(mock_get_processes.call_count, 2)

        mock_create_snapshot.assert_called_once_with(self.user, [{"pid": 1234, "status": "running"}])


class TestSnapshotDetailsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.snapshot = Snapshot.objects.create(
            author=self.user,
            process_data=json.dumps([{"pid": 1234, "status": "running"}])
        )

    def test_snapshot_details_view_with_authenticated_user(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("processes:snapshot_detail", args=[self.snapshot.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "processes/snapshot_detail.html")
        self.assertContains(response, "running")
