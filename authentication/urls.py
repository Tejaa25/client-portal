from django.urls import path
from .views import CustomLoginView, RegisterPage, CustomLogoutView, ForgotPasswordView, ChangePasswordView, AddEmployeeView, SetPasswordView
from django.contrib.auth import views as auth_views
# Create your tests here.

urlpatterns = [
    path('reset_password/',
         auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='authentication/password_reset_done.html'
         ), name='passresetdone'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('change_password/<str:token>/',
         ChangePasswordView.as_view(), name="change_password"),
    path('set_password/<str:token>/',
         SetPasswordView.as_view(), name="set_password"),
    path('addemployee/', AddEmployeeView.as_view(), name="add_employee")

    # path('change_password/<token>/', change_password)
]
