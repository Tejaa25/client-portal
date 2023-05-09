from django.db import models
from authentication.models import CustomUser
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    task = models.CharField(max_length=50)
    task_detail = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateField()
    role = models.CharField(max_length=3, choices=CustomUser.role_choices)
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='assigned_to', null=True, blank=True)

    def __str__(self):
        return self.task
