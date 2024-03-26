from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.permissions import IsAdminOrAuthorOrReadOnly
from api.v1.users.serializers import (
    UserSubscribeSerializer, UserSubscribeRepresentSerializer
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Пользователь."""

    @action(
        detail=False, methods=('GET',), permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserSubscribeView(APIView):
    """Подписка на пользователя."""

    permission_classes = (IsAdminOrAuthorOrReadOnly,)

    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        serializer = UserSubscribeSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
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
    """Получение списка всех подписок на пользователей."""

    serializer_class = UserSubscribeRepresentSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)
