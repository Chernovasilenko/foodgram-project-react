from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.permissions import CurrentUserOrAdmin
from djoser.views import UserViewSet
from djoser.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.users.serializers import (
    UserSubscribeSerializer, UserSubscribeRepresentSerializer
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет для профиля."""

    def get_permissions(self):
        """Добавляет возможность настройки разрешений для эндпоинта 'me'."""
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.user_me
        return super().get_permissions()

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от запроса."""
        if self.action == 'subscriptions':
            return UserSubscribeRepresentSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """Выбор кверисета в зависимости от запроса."""
        if self.action == 'subscriptions':
            return User.objects.filter(following__user=self.request.user)
        return super().get_queryset()

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(CurrentUserOrAdmin,)
    )
    def subscribe(self, request, **kwargs):
        """Подписаться на пользователя."""
        serializer = UserSubscribeSerializer(
            data={
                'user': request.user.id,
                'author': get_object_or_404(User, id=kwargs.get('id')).id
            },
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, **kwargs):
        """Отписаться от пользователя."""
        follower = request.user.follower.filter(
            author=get_object_or_404(User, id=kwargs.get('id'))
        )
        if not follower:
            return Response(
                {'error': 'Нет подписки на этого пользователя!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follower.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        url_path='subscriptions',
        permission_classes=(CurrentUserOrAdmin,)
    )
    def subscriptions(self, request, *args, **kwargs):
        """Подписки пользователя."""
        return self.list(request, *args, **kwargs)
