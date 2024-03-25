from django.urls import include, path

# from foodgram.settings import API_VER

app_name = 'api'

urlpatterns = [
    path('', include('api.v1.urls')),
]
