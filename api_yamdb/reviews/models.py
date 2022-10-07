from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
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


class Category(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=False)


class Genre(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=False)


class Title(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    year = models.IntegerField()
    description = models.TextField(null=False, blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(Category, related_name='titles', on_delete=models.DO_NOTHING)
