import pytest
from auctions.models import User, Listing


@pytest.fixture
def create_user(db):
    # Default user
    def make_user(
        username="testuser", password="password123", email="test@example.com"
    ):
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return user

    return make_user


@pytest.fixture
def authenticated_client(client, create_user):
    user = create_user()
    client.login(username="testuser", password="password123")
    return client, user


@pytest.fixture
def create_listing(db, create_user):
    def make_listing(
        title="title", description="description", bid=500, category=None, user=None
    ):
        if user is None:
            user = create_user()
        listing = Listing.objects.create(
            title=title,
            description=description,
            starting_bid=bid,
            category=category,
            created_by=user,
        )
        return listing

    return make_listing
