from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        'Роль пользователя',
        max_length=15,
        choices=ROLE_CHOICES,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=6,
        default=''
    )
    password = models.CharField(
        'Пароль',
        max_length=255,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        blank=False,
        unique=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
