from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


from users.models import Subscribe

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Администрирование пользователей."""

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    list_display_links = ('username',)
    filter_horizontal = ('user_permissions',)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Администрирование подписок."""

    list_display = ('id', 'user', 'author', 'created')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')


admin.site.unregister(Group)
admin.site.site_title = 'Административный сайт Foodgram'
admin.site.site_header = 'Администрирование Foodgram'
admin.site.empty_value_display = 'Не задано'
