from django.urls import path
from .views import Tasklist, TaskCreate, TaskDelete, TaskDetail, TaskUpdate, AssignedTask, UnAssignedTask, AssignedTaskUpdate, AsssignedTaskDelete, HomePage, CompletedTask, PendingTask
from .views import HomePage1
# Create your tests here.

urlpatterns = [
    path('home/', HomePage1.as_view(), name="home1"),
    path('', HomePage.as_view(), name="home"),
    path('tasks/', Tasklist.as_view(), name='tasklist'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='taskdetail'),
    path('taskcreate', TaskCreate.as_view(), name='taskcreate'),
    path('taskupdate/<int:pk>/', TaskUpdate.as_view(), name='taskupdate'),
    path('assignedtaskupdate/<int:pk>/',
         AssignedTaskUpdate.as_view(), name='assignedtaskupdate'),
    path('taskdelete/<int:pk>/', TaskDelete.as_view(), name='taskdelete'),
    path('assignedtaskdelete/<int:pk>/',
         AsssignedTaskDelete.as_view(), name='assigned_taskdelete'),
    path('assigned_task/', AssignedTask.as_view(), name="assigned_task"),
    path('unassigned_task/', UnAssignedTask.as_view(), name="unassigned_task"),
    path('completedtasks/', CompletedTask.as_view(), name='completed_task'),
    path('pendingtasks/', PendingTask.as_view(), name='pending_task')

]
