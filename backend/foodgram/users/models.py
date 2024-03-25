from django.contrib.auth.models import AbstractUser
from django.db import models

from core import constants as const
from users.validators import username_validator


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        verbose_name='username',
        max_length=const.MAX_LENGHT_NAME_FIELD,
        unique=True,
        validators=(username_validator,)
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=const.MAX_LENGHT_CHAR_FIELD,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=const.MAX_LENGHT_NAME_FIELD
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=const.MAX_LENGHT_NAME_FIELD
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Модель взаимосвязи пользователей."""

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following'
    )
    created = models.DateTimeField(
        verbose_name='Дата и время подписки',
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(fields=('-created',)),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-created',)
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_author',
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
