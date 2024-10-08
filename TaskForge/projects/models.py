from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    users = models.ManyToManyField(User, related_name='projects')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
