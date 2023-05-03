from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.


class CustomUser(AbstractUser):
    PROJECT_MANAGER = "PM"
    FRONTEND_DEV = "FD"
    BACKEND_DEV = "BD"
    UI_UX_DESIGNER = "UD"
    SEARCH_ENGINE_OPTIMIZATION = "SEO"
    role_choices = [(PROJECT_MANAGER, 'project manager'),
                    (FRONTEND_DEV, 'frontend developer'),
                    (BACKEND_DEV, 'backend developer'),
                    (UI_UX_DESIGNER, 'ui/ux designer'),
                    (SEARCH_ENGINE_OPTIMIZATION, 'SEO',)]
    role = models.CharField(
        max_length=3, choices=role_choices)
