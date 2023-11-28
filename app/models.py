from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    projectName = models.CharField(max_length=200)
    bio = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.projectName
