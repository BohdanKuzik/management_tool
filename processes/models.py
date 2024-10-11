from django.db import models
from django.contrib.auth.models import User


class Snapshot(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    process_data = models.JSONField()

    def __str__(self):
        return f"Snapshot by {self.author} at {self.timestamp}"
