from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
