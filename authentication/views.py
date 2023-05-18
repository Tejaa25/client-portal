from django.views import View
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login, get_user_model, authenticate
from .forms import CustomUserCreationForm, ForgetPasswordForm, ChangePasswordForm, AddEmployeeForm, SetPasswordForm
from .models import CustomUser
from .helpers import send_forget_password_mail, send_set_password_mail
import uuid
from django.contrib import messages

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    fields = ['__all__',]

    def get_success_url(self):
        return reverse('home')


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
            messages.success(
                self.request, 'Registration successful! You can now log in.')
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
            email = request.POST["email"]
            if not CustomUser.objects.filter(email=email).first():
                messages.warning(self.request, "Mail id is not present")
                return redirect('forgot_password')
            user_obj = CustomUser.objects.get(email=email)
            if not user_obj.forget_password_token:
                token = str(uuid.uuid4())
                user_obj.forget_password_token = token
                user_obj.save()
            else:
                token = user_obj.forget_password_token
            mail_sent = send_forget_password_mail(user_obj.email, token)
            if mail_sent:
                messages.success(
                    self.request, 'mail sent successfully.')
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
                    messages.success(
                        self.request, 'Password changed successfully! You can now log in.')
                    return redirect('/')
            else:
                messages.warning(
                    self.request, "enter same password in password confirmation as you entered before")
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
            user.email = request.POST["email"]
            user.role = request.POST["role"]
            token = str(uuid.uuid4())
            user.forget_password_token = token
            user.created_by = request.user.pk
            user.save()
            mail_sent = send_set_password_mail(user.email, token)
            if mail_sent:
                messages.success(self.request, "Employee added successfully")
                return redirect('/')
            context = {'form': form}
            return render(request, self.template_name, context)


class SetPasswordView(View):
    template_name = 'authentication/set_password.html'
    success_url = '/'

    def get(self, request, token):
        context = {'form': SetPasswordForm()}
        return render(request, self.template_name, context)

    def post(self, request, token):
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            new_password1 = request.POST["password1"]
            new_password2 = request.POST["password2"]
            if new_password1 and new_password2 and new_password1 == new_password2:
                profile_obj = CustomUser.objects.filter(
                    forget_password_token=token).first()
                if profile_obj:
                    profile_obj.set_password(new_password1)
                    profile_obj.forget_password_token = ''
                    profile_obj.username = request.POST["username"]
                    profile_obj.first_name = request.POST["first_name"]
                    profile_obj.last_name = request.POST["last_name"]
                    profile_obj.save()
                    messages.success(
                        self.request, 'Password set to your account successfully! You can now log in.')
                    return redirect('/')
        context = {'form': form}
        return render(request, self.template_name, context)
