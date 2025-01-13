from django.db import models
from django.utils.timezone import now

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    task_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default="Ongoing")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
