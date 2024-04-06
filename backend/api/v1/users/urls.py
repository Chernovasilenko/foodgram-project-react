from django.urls import include, path
from rest_framework import routers

from api.v1.users import views

router_users_v1 = routers.DefaultRouter()

router_users_v1.register(r'users', views.CustomUserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_users_v1.urls)),
]
