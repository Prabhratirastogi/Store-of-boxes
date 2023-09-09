from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Box(models.Model):
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
