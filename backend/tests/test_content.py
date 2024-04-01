import pytest

from rest_framework import status

pytestmark = pytest.mark.django_db


def test_get_me_with_auth_user(author_client, author):
    r = author_client.get('/api/users/me/')
    assert r.json() == {
        "email": author.email,
        "id": author.pk,
        "username": author.username,
        "first_name": author.first_name,
        "last_name": author.last_name,
        "is_subscribed": False,
    }
