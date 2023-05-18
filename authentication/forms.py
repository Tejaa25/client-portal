from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=20, required=True, help_text='Required...')
    last_name = forms.CharField(
        max_length=20, required=True, help_text='Required...')
    email = forms.EmailField(
        max_length=254, required=True, help_text='Enter your valid email address')

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + \
            ('first_name', 'last_name',
             'email')  # backslash helps us to continue our code on the next line


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=254, required=True, help_text='Enter your valid email address')


class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(min_length=8,
                                label="Password",
                                widget=forms.PasswordInput,
                                strip=False,
                                help_text="Enter a strong password.",
                                )
    password2 = forms.CharField(min_length=8,
                                label="Password confirmation",
                                strip=False,
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as before, for verification.",)


class SetPasswordForm(forms.Form):
    username = forms.CharField(min_length=4)
    first_name = forms.CharField(
        max_length=20, required=True, help_text='Required...')
    last_name = forms.CharField(
        max_length=20, required=True, help_text='Required...')
    password1 = forms.CharField(min_length=8,
                                label="Password",
                                widget=forms.PasswordInput,
                                strip=False,
                                help_text="Enter a strong password.",
                                )
    password2 = forms.CharField(min_length=8,
                                label="Password confirmation",
                                strip=False,
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as before, for verification.",)


class AddEmployeeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'role')

# class CustomUserCreationForm(forms.ModelForm):
#     username = forms.CharField(min_length=4)
#     first_name = forms.CharField(min_length=2)
#     last_name = forms.CharField(min_length=2)
#     password1 = forms.CharField(min_length=8,
#                                 label="Password",
#                                 widget=forms.PasswordInput,
#                                 strip=False,
#                                 help_text="Enter a strong password.",
#                                 )
#     password2 = forms.CharField(min_length=8,
#                                 label="Password confirmation",
#                                 strip=False,
#                                 widget=forms.PasswordInput,
#                                 help_text="Enter the same password as before, for verification.",
#                                 )

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'first_name', 'last_name', 'email',
#                   'password1', 'password2')

#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 ("The two password fields didn't match."))
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
