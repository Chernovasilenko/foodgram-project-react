from django.urls import include, path
from rest_framework import routers

from api.v1.users import views

router_users_v1 = routers.DefaultRouter()

router_users_v1.register(r'users', views.CustomUserViewSet, basename='me')


urlpatterns = [
    path(
        'users/subscriptions/',
        views.UserSubscriptionsViewSet.as_view({'get': 'list'}),
    ),
    path(
        'users/<int:user_id>/subscribe/',
        views.UserSubscribeView.as_view(),
    ),
    path('', include(router_users_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
