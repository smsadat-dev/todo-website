from django.contrib.auth.models import User
from django.db import models

# Task Model

class TaskModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    creationTime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
