from django.contrib import admin
# from .models import CustomUser
from django.contrib.auth import get_user_model
# Register your models here.
CustomUser = get_user_model()
admin.site.register(CustomUser)
