from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model
# from clientportal import settings
# from .models import UserProfile


class CustomUserCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=20, required=True, help_text='Required...')
    last_name = forms.CharField(
        max_length=20, required=True, help_text='Required...')
    email = forms.EmailField(
        max_length=254, required=True, help_text='Enter your valid email address')
    role = forms.ChoiceField(choices=CustomUser.role_choices)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter a strong password.",
    )
    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email',
                  'role', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data["role"]
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 == password2:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(
#         max_length=20, required=True, help_text='Required...')
#     last_name = forms.CharField(
#         max_length=20, required=True, help_text='Required...')
#     email = forms.EmailField(
#         max_length=254, required=True, help_text='Enter your valid email address')
#     role = forms.ChoiceField(choices=CustomUser.role_choices)

#     class Meta:
#         model = CustomUser
#         fields = UserCreationForm.Meta.fields + \
#             ('first_name', 'last_name', 'email',
#              'role')  # backslash helps us to continue our code on the next line

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.email = self.cleaned_data['email']
#         user.role = self.cleaned_data["role"]
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
