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
    name = models.CharField(max_length=256, null=False, blank=False)
    slug = models.SlugField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
    )


class Genre(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    slug = models.SlugField(
        max_length=50,
        null=False,
        blank=False,
        unique=True
    )


class Title(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    year = models.IntegerField()
    description = models.TextField(null=False, blank=True)
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.DO_NOTHING
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    # !!!Этот код все ломает, зачем он тут?
    # class Meta:
    #     verbose_name = 'Отзыв',
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=('title', 'author'),
    #             name='unique review')]
    #     ordering = ('pub_date',)
    #     unique_together = ('genre', 'title', )
    #
    # def __str__(self):
    #     return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.CharField(
        verbose_name='Текст комментария',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
