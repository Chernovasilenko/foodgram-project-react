from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.permissions import CurrentUserOrAdmin
from djoser.views import UserViewSet
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.users.serializers import (
    UserSubscribeSerializer, UserSubscribeRepresentSerializer
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Вьюсет для профиля."""

    @action(
        detail=False, methods=('get',), permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Получение данных пользователя."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserSubscribeView(APIView):
    """Вьюсет для подписки на пользователя."""

    permission_classes = (CurrentUserOrAdmin,)

    def post(self, request, user_id):
        """Подписаться на пользователя."""
        author = get_object_or_404(User, id=user_id)
        serializer = UserSubscribeSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        """отписаться от пользователя."""
        author = get_object_or_404(User, id=user_id)
        follower = request.user.follower.filter(author=author)
        if not follower:
            return Response(
                {'error': 'Нет подписки на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follower.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscriptionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Вьюсет для списка подписок пользователя."""

    permission_classes = (CurrentUserOrAdmin,)
    serializer_class = UserSubscribeRepresentSerializer

    def get_queryset(self):
        """Получает подписчиков пользователя."""
        return User.objects.filter(following__user=self.request.user)
