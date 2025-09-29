import pytest
from django.urls import reverse
from auctions.models import User


@pytest.mark.django_db
def test_register_success(client):
    response = client.post(
        reverse("register"),
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "confirmation": "password123",
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("index")
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_register_password_mismatch(client):
    response = client.post(
        reverse("register"),
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "confirmation": "different",
        },
    )
    assert response.status_code == 200
    assert b"Passwords must match." in response.content
    assert not User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_register_username_taken(client, create_user):
    create_user(username="existing")
    response = client.post(
        reverse("register"),
        {
            "username": "existing",
            "email": "existing@example.com",
            "password": "password123",
            "confirmation": "password123",
        },
    )
    assert response.status_code == 200
    assert b"Username already taken." in response.content


@pytest.mark.django_db
def test_login_success(client, create_user):
    create_user(username="loginuser", password="pass1234")
    response = client.post(
        reverse("login"),
        {
            "username": "loginuser",
            "password": "pass1234",
        },
    )
    assert response.status_code == 302
    assert response.url == reverse("index")


@pytest.mark.django_db
def test_login_invalid_credentials(client):
    response = client.post(
        reverse("login"),
        {
            "username": "unknown",
            "password": "wrong",
        },
    )
    assert response.status_code == 200
    assert b"Invalid username and/or password." in response.content


@pytest.mark.django_db
def test_logout(authenticated_client):
    client, _ = authenticated_client
    response = client.get(reverse("logout"))
    assert response.status_code == 302
    assert response.url == reverse("index")
