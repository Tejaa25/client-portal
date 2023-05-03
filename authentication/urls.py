from django.urls import path
from .views import CustomLoginView, RegisterPage, TaskView, CustomLogoutView
# Create your tests here.

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('tasks/', TaskView.as_view(), name='tasklist')
]
