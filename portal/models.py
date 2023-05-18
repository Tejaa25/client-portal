from django.db import models
from authentication.models import CustomUser
from django.db.models import Q
# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    admin = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='admin', null=True, blank=True)
    task = models.CharField(max_length=50)
    task_detail = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    deadline = models.DateField()
    assigned_to = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='assigned_to', null=True, blank=True)

#  static method is a method that belongs to the class itself rather than an instance of the class.
#  It can be called on the class directly without the need for an instance.
    @staticmethod
    def get_task_statistics(self):
        if self.request.user.role == 'PM':
            tasks = Task.objects.filter(user=self.request.user)
            assigned_task = tasks.exclude(assigned_to=None).count()
        # elif self.request.user.role == 'PM':
        #     tasks = Task.objects.filter(
        #         Q(user=self.request.user) | Q(assigned_to=self.request.user))
        #     assigned_task = tasks.filter(assigned_to=self.request.user).count()
        elif self.request.user.role in ['FD', 'BD', 'SEO', 'UD']:
            tasks = Task.objects.filter(assigned_to=self.request.user)
            assigned_task = tasks.filter(assigned_to=self.request.user).count()
        else:
            tasks = Task.objects.filter(admin=self.request.user)
            assigned_task = tasks.exclude(assigned_to=None).count()
        total_tasks = tasks.count()
        unassigned_task = total_tasks-assigned_task
        task_completed = tasks.filter(completed=True).count()
        task_pending = total_tasks-task_completed
        return {
            'total_tasks': total_tasks,
            'assigned_task': assigned_task,
            'unassigned_task': unassigned_task,
            'task_completed': task_completed,
            'task_pending': task_pending,
        }

    def __str__(self):
        return self.task
