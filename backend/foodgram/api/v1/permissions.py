from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    """
    Администратор или автор могут редактировать данные.
    Другие пользователи могут запросить данные.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
            or request.user.is_superuser
        )
