from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login, get_user_model, authenticate
from .forms import CustomUserCreationForm, ForgetPasswordForm, ChangePasswordForm, AddEmployeeForm
from .models import CustomUser
from .helpers import send_forget_password_mail, send_set_password_mail
import uuid

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
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            return redirect('login')
        else:
            return super(RegisterPage, self).form_invalid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super(RegisterPage, self).get(*args, **kwargs)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class ForgotPasswordView(View):
    template_name = 'authentication/forgot_password.html'
    form_class = ForgetPasswordForm
    success_url = 'login/'

    def get(self, request):
        context = {'form': ForgetPasswordForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            if not CustomUser.objects.filter(username=username).first():
                return redirect('forgot_password')
            user_obj = CustomUser.objects.get(username=username)
            if not user_obj.forget_password_token:
                token = str(uuid.uuid4())
                user_obj.forget_password_token = token
                user_obj.save()
            else:
                token = user_obj.forget_password_token
            mail_sent = send_forget_password_mail(user_obj.email, token)
            if mail_sent:
                return redirect('/')
            context = {'form': form}
            return render(request, self.template_name, context)


class ChangePasswordView(View):
    template_name = 'authentication/change_password.html'
    success_url = '/'

    def get(self, request, token):
        context = {'form': ChangePasswordForm()}
        return render(request, self.template_name, context)

    def post(self, request, token):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password1 = request.POST["password1"]
            new_password2 = request.POST["password2"]
            if new_password1 and new_password2 and new_password1 == new_password2:
                profile_obj = CustomUser.objects.filter(
                    forget_password_token=token).first()
                if profile_obj:
                    profile_obj.set_password(new_password1)
                    profile_obj.forget_password_token = ''
                    profile_obj.save()
                    return redirect('/')
        context = {'form': form}
        return render(request, self.template_name, context)


class AddEmployeeView(FormView):
    template_name = 'authentication/add_employee.html'
    success_url = '/'

    def get(self, request):
        context = {'form': AddEmployeeForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            user = CustomUser()
            user.username = request.POST["username"]
            user.email = request.POST["email"]
            token = str(uuid.uuid4())
            user.forget_password_token = token
            user.created_by = request.user.pk
            user.save()
            mail_sent = send_set_password_mail(user.email, token)
            if mail_sent:
                return redirect('/')
            context = {'form': form}
            return render(request, self.template_name, context)


class SetPasswordView(View):
    template_name = 'authentication/change_password.html'
    success_url = '/'

    def get(self, request, token):
        context = {'form': ChangePasswordForm()}
        return render(request, self.template_name, context)

    def post(self, request, token):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password1 = request.POST["password1"]
            new_password2 = request.POST["password2"]
            if new_password1 and new_password2 and new_password1 == new_password2:
                profile_obj = CustomUser.objects.filter(
                    forget_password_token=token).first()
                if profile_obj:
                    profile_obj.set_password(new_password1)
                    profile_obj.forget_password_token = ''
                    profile_obj.save()
                    return redirect('login/')
        context = {'form': form}
        return render(request, self.template_name, context)
