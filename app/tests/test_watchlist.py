import pytest
from django.urls import reverse
from auctions.models import Watchlist


@pytest.mark.django_db
def test_add_listing_to_watchlist(authenticated_client, create_user, create_listing):
    client, user = authenticated_client
    user_listing = create_user(username="toto", email="toto@gmail.com")
    listing = create_listing(title="Tablet", description="iPad", user=user_listing)
    response = client.post(reverse("watchlist_listing", args=[listing.id]))
    assert response.status_code == 302
    user.refresh_from_db()
    assert listing in user.watchlist.listings.all()


@pytest.mark.django_db
def test_remove_listing_from_watchlist(
    authenticated_client, create_user, create_listing
):
    client, user = authenticated_client
    user_listing = create_user(username="toto", email="toto@gmail.com")
    listing = create_listing(title="Tablet", description="iPad", user=user_listing)
    watchlist = Watchlist.objects.create(user=user)
    watchlist.listings.add(listing)

    response = client.post(reverse("watchlist_listing", args=[listing.id]))
    assert response.status_code == 302
    user.refresh_from_db()
    assert listing not in user.watchlist.listings.all()


@pytest.mark.django_db
def test_view_watchlist(authenticated_client, create_user, create_listing):
    client, user = authenticated_client
    user_listing = create_user(username="toto", email="toto@gmail.com")
    listing = create_listing(title="Tablet", description="iPad", user=user_listing)
    watchlist = Watchlist.objects.create(user=user)
    watchlist.listings.add(listing)

    response = client.get(reverse("watchlist"))
    assert response.status_code == 200
    assert listing.title.encode() in response.content
