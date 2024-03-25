from django.urls import include, path

from foodgram.settings import API_VER

app_name = 'api'

urlpatterns = [
    path(f'{API_VER}/', include('api.v1.urls')),
]
