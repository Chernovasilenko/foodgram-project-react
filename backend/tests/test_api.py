import pytest

from rest_framework import status
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db


CLIENT = lazy_fixture('api_client')
AUTHOR = lazy_fixture('author_client')
ANOTHER_AUTHOR = lazy_fixture('another_author_client')
USER_SUB = lazy_fixture('author_sub_client')

URL_API = '/api/'
URL_RECIPES = '/api/recipes/'
URL_RECIPE_ID = '/api/recipes/'
URL_NOT_EXIST_RECIPE = '/api/recipes/9999/'
URL_TAGS = '/api/tags/'
URL_TAG_ID = lazy_fixture('tag_url')
URL_NOT_EXIST_TAG = '/api/tags/9999/'
URL_INGRIDIENTS = '/api/ingredients/'
URL_INGRIDIENT_ID = lazy_fixture('ingredient_url_id')
URL_INGRIDIENT_NAME = lazy_fixture('ingredient_url_name')
URL_RECIPE_FAVORITE = lazy_fixture('add_recipe_to_favorite_url')
URL_DL_SHOPCART = '/api/recipes/download_shopping_cart/'
URL_ADD_SHOPCART = lazy_fixture('add_recipe_to_shopcart_url')
URL_USERS = '/api/users/'
URL_USER_DETAIL = lazy_fixture('user_detail_url')
URL_NOT_EXIST_USER_DETAIL = '/api/users/9999/'
URL_USER_ME = '/api/users/me/'
URL_SET_PASSWORD = '/api/users/set_password/'
URL_TOKEN_LOGIN = '/api/auth/token/login/'
URL_TOKEN_LOGOUT = '/api/auth/token/logout/'
URL_SUBSCRIPTIONS = '/api/users/subscriptions/'
URL_SUBSCRIBE = lazy_fixture('user_subscribe_url')
URL_NOT_FOUND_SUBSCRIBE = '/api/users/9999/subscribe/'


@pytest.mark.parametrize(
    'url, user, expected_status, method',
    (
        (URL_API, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_RECIPES, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_RECIPES, CLIENT, status.HTTP_401_UNAUTHORIZED, 'POST'),
        (URL_RECIPE_ID, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_NOT_EXIST_RECIPE, CLIENT, status.HTTP_404_NOT_FOUND, 'GET'),
        (URL_RECIPE_ID, CLIENT, status.HTTP_401_UNAUTHORIZED, 'PUT'),
        (URL_TAGS, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_TAG_ID, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_TAG_ID, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_INGRIDIENTS, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_INGRIDIENT_NAME, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_RECIPE_FAVORITE, CLIENT, status.HTTP_401_UNAUTHORIZED, 'POST'),
        (URL_RECIPE_FAVORITE, CLIENT, status.HTTP_401_UNAUTHORIZED, 'DELETE'),
        (URL_RECIPE_FAVORITE, AUTHOR, status.HTTP_201_CREATED, 'POST'),
        (URL_RECIPE_FAVORITE, USER_SUB, status.HTTP_204_NO_CONTENT, 'DELETE'),
        (URL_RECIPE_FAVORITE, USER_SUB, status.HTTP_400_BAD_REQUEST, 'POST'),
        (URL_RECIPE_FAVORITE, AUTHOR, status.HTTP_400_BAD_REQUEST, 'DELETE'),
        (URL_DL_SHOPCART, CLIENT, status.HTTP_401_UNAUTHORIZED, 'GET'),
        (URL_DL_SHOPCART, AUTHOR, status.HTTP_400_BAD_REQUEST, 'GET'),
        (URL_DL_SHOPCART, USER_SUB, status.HTTP_200_OK, 'GET'),
        (URL_ADD_SHOPCART, CLIENT, status.HTTP_401_UNAUTHORIZED, 'GET'),
        (URL_ADD_SHOPCART, CLIENT, status.HTTP_401_UNAUTHORIZED, 'DELETE'),
        (URL_ADD_SHOPCART, AUTHOR, status.HTTP_201_CREATED, 'POST'),
        (URL_ADD_SHOPCART, USER_SUB, status.HTTP_400_BAD_REQUEST, 'POST'),
        (URL_ADD_SHOPCART, AUTHOR, status.HTTP_400_BAD_REQUEST, 'DELETE'),
        (URL_ADD_SHOPCART, USER_SUB, status.HTTP_204_NO_CONTENT, 'DELETE'),
        (URL_USERS, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_USER_DETAIL, CLIENT, status.HTTP_200_OK, 'GET'),
        (URL_USER_DETAIL, AUTHOR, status.HTTP_200_OK, 'GET'),
        (URL_USER_DETAIL, ANOTHER_AUTHOR, status.HTTP_200_OK, 'GET'),
        (URL_USER_ME, AUTHOR, status.HTTP_200_OK, 'GET'),
        (URL_NOT_EXIST_USER_DETAIL, CLIENT, status.HTTP_404_NOT_FOUND, 'GET'),
        (URL_SUBSCRIPTIONS, CLIENT, status.HTTP_401_UNAUTHORIZED, 'GET'),
        (URL_SUBSCRIPTIONS, AUTHOR, status.HTTP_200_OK, 'GET'),
        (URL_SUBSCRIBE, CLIENT, status.HTTP_401_UNAUTHORIZED, 'POST'),
        (URL_SUBSCRIBE, CLIENT, status.HTTP_401_UNAUTHORIZED, 'DELETE'),
        (URL_SUBSCRIBE, ANOTHER_AUTHOR, status.HTTP_201_CREATED, 'POST'),
        (URL_SUBSCRIBE, USER_SUB, status.HTTP_400_BAD_REQUEST, 'POST'),
        (URL_SUBSCRIBE, USER_SUB, status.HTTP_204_NO_CONTENT, 'DELETE'),
        (URL_SUBSCRIBE, USER_SUB, status.HTTP_400_BAD_REQUEST, 'POST'),
        (URL_NOT_FOUND_SUBSCRIBE, AUTHOR, status.HTTP_404_NOT_FOUND, 'DELETE'),
        (URL_NOT_FOUND_SUBSCRIBE, AUTHOR, status.HTTP_404_NOT_FOUND, 'DELETE'),
        (URL_SET_PASSWORD, CLIENT, status.HTTP_401_UNAUTHORIZED, 'POST'),
        (URL_TOKEN_LOGOUT, AUTHOR, status.HTTP_204_NO_CONTENT, 'POST'),
        (URL_TOKEN_LOGOUT, CLIENT, status.HTTP_401_UNAUTHORIZED, 'POST'),
    ),
)
def test_endpoints(
    url, user, expected_status, method
):
    """Проверка доступа к эндпоинтам."""
    if method == 'GET':
        response = user.get(url)
    if method == 'POST':
        response = user.post(url)
    if method == 'PUT':
        response = user.put(url)
    if method == 'DELETE':
        response = user.delete(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url, user, expected_status, data',
    (
        (
            URL_USERS, CLIENT, status.HTTP_201_CREATED,
            {
                'email': 'test_user@ya.ru',
                'username': 'testik',
                'first_name': 'Test',
                'last_name': 'Testovoi',
                'password': 'passworTest0104',
            }
        ),
        (
            URL_USERS, CLIENT, status.HTTP_400_BAD_REQUEST,
            {
                'email': 'test_user@ya.ru',
                'username': 'testik',
            }
        ),
        (
            URL_SET_PASSWORD, AUTHOR, status.HTTP_204_NO_CONTENT,
            {
                'new_password': 'thi$Pa$$w0rdW@sCh@nged',
                'current_password': 'MySecretPas$word',
            }
        ),
        (
            URL_SET_PASSWORD, AUTHOR, status.HTTP_400_BAD_REQUEST,
            {
                'new_password': 'new_password',
            }
        ),
        (
            URL_TOKEN_LOGIN, AUTHOR, status.HTTP_200_OK,
            {
                'password': 'MySecretPas$word',
                'email': 'test_user@ya.ru'
            }
        ),
        (
            URL_TOKEN_LOGIN, AUTHOR, status.HTTP_400_BAD_REQUEST,
            {
                'password': 'WrongPassword',
                'email': 'test_user@ya.ru'
            }
        ),
    ),
)
def test_endpoints_with_data(
    url, user, expected_status, data
):
    """Проверка POST-запросов."""
    response = user.post(url, data)
    assert response.status_code == expected_status
