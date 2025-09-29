import pytest
from django.urls import reverse
from auctions.models import Listing, Category


@pytest.mark.django_db
def test_index_view_shows_active_listings(client, create_listing):
    category = Category.objects.create(name="Electronics")
    _ = create_listing(
        title="Phone",
        description="Nice phone",
        bid=100,
        category=category,
    )
    response = client.get(reverse("index"))
    assert response.status_code == 200
    assert b"Phone" in response.content


@pytest.mark.django_db
def test_create_listing_get(authenticated_client):
    client, _ = authenticated_client
    response = client.get(reverse("create_listing"))
    assert response.status_code == 200
    assert b"Create a New Listing" in response.content


@pytest.mark.django_db
def test_create_listing_success(authenticated_client):
    client, _ = authenticated_client
    category = Category.objects.create(name="Books")
    response = client.post(
        reverse("create_listing"),
        {
            "title": "Django Book",
            "description": "Learn Django",
            "starting_bid": 50,
            "image_url": "",
            "category": category.id,
        },
    )

    listing = Listing.objects.first()
    assert response.status_code == 302
    assert response.url == reverse("listing", args=[listing.id])
    assert listing.title == "Django Book"


@pytest.mark.django_db
def test_create_listing_invalid_fields(authenticated_client):
    client, _ = authenticated_client

    response = client.post(
        reverse("create_listing"),
        {
            "title": "x" * 101,
            "description": "y" * 501,
            "starting_bid": -1,
        },
    )

    assert response.status_code == 200
    assert b"Title must be between 1 and 100 characters." in response.content
    assert b"Description must be between 1 and 500 characters." in response.content
    assert b"Starting bid must be greater than $0." in response.content


@pytest.mark.django_db
def test_listing_view_valid(client, create_listing):
    listing = create_listing(
        title="Camera",
        description="Good camera",
        bid=200,
    )
    response = client.get(reverse("listing", args=[listing.id]))
    assert response.status_code == 200
    assert b"Camera" in response.content


@pytest.mark.django_db
def test_listing_view_not_found(client):
    response = client.get(reverse("listing", args=[999]))
    assert response.status_code == 404 or b"not found" in response.content


@pytest.mark.django_db
def test_listing_view_make_correct_bid_and_comment(
    authenticated_client, create_user, create_listing
):
    client, _ = authenticated_client
    user2 = create_user(username="Amine", email="amine@gmail.com")

    listing = create_listing(
        title="Camera",
        description="Good camera",
        bid=200,
        user=user2,
    )

    response = client.post(reverse("listing", args=[listing.id]), {"bid": 300})

    assert response.status_code == 302
    assert response.url == reverse("listing", args=[listing.id])

    response = client.post(
        reverse("listing", args=[listing.id]), {"comment": "test comment"}
    )

    assert response.status_code == 302
    assert response.url == reverse("listing", args=[listing.id])

    listing.refresh_from_db()

    assert listing.current_price() == float(300)

    response = client.get(reverse("listing", args=[listing.id]))

    assert b"Your bid is the current bid." in response.content
    assert b"test comment" in response.content


@pytest.mark.django_db
def test_listing_view_make_incorrect_bid(
    authenticated_client, create_user, create_listing
):
    client, _ = authenticated_client
    user2 = create_user(username="Amine", email="amine@gmail.com")

    listing = create_listing(
        title="Camera",
        description="Good camera",
        user=user2,
    )

    response = client.post(reverse("listing", args=[listing.id]), {"bid": 150})

    assert b"Bid must be greater than the current price:" in response.content


@pytest.mark.django_db
def test_close_listing_success(authenticated_client, create_listing):
    client, user = authenticated_client
    listing = create_listing(title="Tablet", description="iPad", user=user)
    response = client.post(reverse("close_listing", args=[listing.id]))
    listing.refresh_from_db()
    assert response.status_code == 302
    assert not listing.is_active


@pytest.mark.django_db
def test_close_listing_not_owner(authenticated_client, create_user, create_listing):
    client, _ = authenticated_client
    other_user = create_user(username="other")
    listing = create_listing(
        title="Tablet",
        description="iPad",
        bid=300,
        user=other_user,
    )
    response = client.post(reverse("close_listing", args=[listing.id]))
    listing.refresh_from_db()
    assert response.status_code == 302
    assert listing.is_active
