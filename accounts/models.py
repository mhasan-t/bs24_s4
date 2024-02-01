from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField('email', unique=True)
    full_name = models.CharField(
        verbose_name="Full Name", max_length=255, null=False)
    # user_type : 0 = None, 1 = Employee, 2 = Restaurant Managers
    user_type = models.IntegerField(
        default=0, validators=[MaxValueValidator(3)])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.full_name} ({self.email})'
