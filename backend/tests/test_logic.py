import pytest

from rest_framework import status

pytestmark = pytest.mark.django_db


def test_user_registration(api_client):
    data = {
        'email': 'test_user@yandex.ru',
        'username': 'testik',
        'first_name': 'Test',
        'last_name': 'Testovoi',
        'password': 'passworTest0104',
    }
    r = api_client.post('/api/users/', data=data)
    assert r.status_code == status.HTTP_201_CREATED


def test_user_registration_with_error_data(api_client):
    data = {
        'email': 'test_user@yandex.ru',
        'username': 'testik',
    }
    r = api_client.post('/api/users/', data=data)
    assert r.status_code == status.HTTP_400_BAD_REQUEST


# def test_change_password_with_auth_user(author_client):
#     data = {
#         'new_password': 'NewPass2365',
#         'current_password': 'qaZ171786T',
#     }
#     r = author_client.post('/api/users/set_password/', data=data)
#     assert r.json() == '0'
#     assert r.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_with_auth_user_with_error(author_client):
    data = {
        'new_password': 'new_password',
    }
    r = author_client.post('/api/users/set_password/', data=data)
    assert r.status_code == status.HTTP_400_BAD_REQUEST


# def test_get_token(api_client, author):
#     data = {
#         'password': author.password,
#         'email': author.email
#     }
#     r = api_client.post('/api/auth/token/login/', data=data)
#     assert r.json() == '0'
#     assert r.status_code == status.HTTP_200_OK


# def test_create_recipe_with_auth_user(author_client, ingredient, tag):
#     data = {
#         "tags": [tag.pk],
#         "name": "test",
#         "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAA"
#                     "BieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw"
#                     "4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
#         "text": "test",
#         "cooking_time": 1,
#         "ingredients": [
#             {"id": ingredient.pk, "amount": 10}
#         ]
#     }

#     r = author_client.post('/api/recipes/', data=data)
#     assert r.json() == '0'
#     assert r.status_code == status.HTTP_201_CREATED

#     r = author_client.post('/api/recipes/', data=data)
#     assert r.status_code == status.HTTP_400_BAD_REQUEST
