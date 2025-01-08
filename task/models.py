from django.db import models
from typing import Iterable

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task_type = models.CharField(max_length=100,choices=(("Official","Official"),("Normal","Normal")))

