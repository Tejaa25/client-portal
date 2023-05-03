from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login, get_user_model, authenticate
from .forms import CustomUserCreationForm

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    fields = ['__all__',]

    def get_success_url(self):
        return reverse('tasklist')


class RegisterPage(FormView):
    template_name = 'authentication/register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    # 2.If we are reversing inside a function we can use reverse().
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('taskslist')
        return super(RegisterPage, self).get(*args, **kwargs)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class TaskView(ListView):
    pass
