
from django.contrib.auth import backends, get_user_model

User = get_user_model()


class EmailOrUsernameModelBackend(backends.ModelBackend):
    """Авторизация через emeil или username."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Выбирает, через emeil или username авторизовать пользователя."""
        user = User._default_manager.filter(email=username).first()
        if user:
            username = user.username
        return super().authenticate(request, username, password, **kwargs)
