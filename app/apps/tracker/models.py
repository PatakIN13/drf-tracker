import uuid

from django.db import models


# Create your models here.

class UsersTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UsersTask, on_delete=models.CASCADE, related_name='TASKS_USER')
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    activity = models.IntegerField(default=0, blank=True, null=True)
    start_activity_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.description} - {self.user} - {self.activity}"
