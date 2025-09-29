import pytest
from auctions.forms import BidForm, CommentForm, ListingForm
from auctions.models import Category


@pytest.mark.django_db
def test_bid_form_valid():
    form = BidForm(data={"bid": "10.50"})
    assert form.is_valid()


@pytest.mark.django_db
def test_bid_form_invalid_too_low():
    form = BidForm(data={"bid": "0"})
    assert not form.is_valid()
    assert "bid" in form.errors
    assert form.errors["bid"] == ["Ensure this value is greater than or equal to 0.01."]


@pytest.mark.django_db
def test_comment_form_valid():
    form = CommentForm(data={"comment": "This is a test comment"})
    assert form.is_valid()


@pytest.mark.django_db
def test_comment_form_required():
    form = CommentForm(data={"comment": ""})
    assert not form.is_valid()
    assert form.errors["comment"] == ["Comment must not be empty."]


@pytest.mark.django_db
def test_comment_form_too_long():
    form = CommentForm(data={"comment": "x" * 501})
    assert not form.is_valid()
    assert form.errors["comment"] == ["Comment must contain less than 500 characters."]


@pytest.mark.django_db
def test_listing_form_valid():
    category = Category.objects.create(name="Electronics")
    form = ListingForm(
        data={
            "title": "iPhone 14",
            "description": "Brand new iPhone",
            "starting_bid": "100",
            "image_url": "http://example.com/image.jpg",
            "category": category.id,
        }
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_listing_form_missing_required_fields():
    form = ListingForm(data={})
    assert not form.is_valid()
    assert "title" in form.errors
    assert "description" in form.errors
    assert "starting_bid" in form.errors


@pytest.mark.django_db
def test_listing_form_invalid_values():
    form = ListingForm(
        data={
            "title": "x" * 101,
            "description": "y" * 501,
            "starting_bid": "0",
            "image_url": "not-a-url",
        }
    )
    assert not form.is_valid()
    assert "title" in form.errors
    assert "description" in form.errors
    assert "starting_bid" in form.errors
    assert "image_url" in form.errors
