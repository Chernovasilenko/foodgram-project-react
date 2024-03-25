from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Subscribe

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Администрирование пользователей."""

    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    list_display_links = ('username',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author', 'created')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


admin.site.site_title = 'Административный сайт Foodgram'
admin.site.site_header = 'Администрирование Foodgram'
admin.site.empty_value_display = 'Не задано'
