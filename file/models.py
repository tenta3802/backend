from django.db import models

from group.models import Group

class File(models.Model):
    name = models.CharField(max_length=128)
    os = models.CharField(max_length=1)
    type = models.CharField(max_length=128)
    creted_at = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)