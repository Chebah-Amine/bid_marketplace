from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms

from .models import User, Listing, Category, Bid, Comment, Watchlist


class BidForm(forms.Form):
    bid = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Bid ($):", min_value=0.01
    )


class CommentForm(forms.Form):
    comment = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Add a comment..."}),
        label="Comment",
    )


class ListingForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label="Title",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter the title"}
        ),
    )
    description = forms.CharField(
        max_length=500,
        label="Description",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Describe your listing"}
        ),
    )
    starting_bid = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Starting Bid ($)",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter starting bid"}
        ),
    )
    image_url = forms.URLField(
        required=False,
        label="Image URL",
        widget=forms.URLInput(
            attrs={"class": "form-control", "placeholder": "Optional image URL"}
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Category",
        widget=forms.Select(attrs={"class": "form-control"}),
    )


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {"listings": listings})


@login_required
def create_listing_view(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].strip()
            description = form.cleaned_data["description"].strip()
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]

            errors = False

            # check if fields respect specifications
            if not (1 <= len(title) <= 100):
                form.add_error(
                    "title",
                    "Title must be between 1 and 100 characters.",
                )
                errors = True

            if not (1 <= len(description) <= 500):
                form.add_error(
                    "description",
                    "Description must be between 1 and 500 characters.",
                )
                errors = True

            if float(starting_bid) <= 0:
                form.add_error(
                    "starting_bid",
                    "Starting bid must be greater than $0.",
                )
                errors = True

            if not errors:
                try:
                    new_listing = Listing.objects.create(
                        title=title,
                        description=description,
                        starting_bid=starting_bid,
                        image_url=image_url or None,
                        category=category,
                        created_by=request.user,
                    )
                    messages.success(request, "Listing created successfully!")
                    return redirect("listing", id=new_listing.id)
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")
                    return render(
                        request,
                        "auctions/error.html",
                        {"code": 400, "message": "Error creating a new listing."},
                    )
    else:
        form = ListingForm()

    return render(request, "auctions/create_listing.html", {"form": form})


def listing_view(request, id):
    try:
        listing = get_object_or_404(Listing, id=id)
    except Exception as e:
        return (
            render(request),
            "auctions/error.html",
            {"code": 404, "message": f"Listing with id {id} not found !\n{e}"},
        )

    bid_form = BidForm()
    bid_label = bid_form.fields["bid"].label
    bid_label += f" {listing.bids.count()} bid(s) sor far now."
    highest_bid = listing.highest_bid()

    if highest_bid and highest_bid.bidder == request.user:
        bid_label += " Your bid is the current bid."

    bid_form.fields["bid"].label = bid_label

    comment_form = CommentForm()

    winner = listing.winner(request.user)

    if request.method == "POST" and request.user.is_authenticated:
        print(request.POST)
        if "bid" in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid = bid_form.cleaned_data["bid"]
                if bid > listing.current_price():
                    Bid.objects.create(listing=listing, bidder=request.user, amount=bid)
                    messages.success(request, "Your bid was successfully placed!")
                    return redirect("listing", id=id)
                else:
                    bid_form.add_error(
                        "bid",
                        f"Bid must be greater than the current price: {listing.current_price()}$.",
                    )
        elif "comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment_text = comment_form.cleaned_data["comment"]
                if comment_text.strip() and len(comment_text) <= 500:
                    Comment.objects.create(
                        listing=listing, commenter=request.user, content=comment_text
                    )
                    messages.success(request, "Your comment was added!")
                    return redirect("listing", id=id)
                else:
                    comment_form.add_error(
                        "comment",
                        "Comment must not be empty and must contain less than 500 characters.",
                    )

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "bid_form": bid_form,
            "comment_form": comment_form,
            "winner": winner,
        },
    )


@login_required
def listing_close_view(request, id):
    try:
        listing = get_object_or_404(Listing, id=id)
    except Exception as e:
        return (
            render(request),
            "auctions/error.html",
            {"code": 404, "message": f"Listing with id {id} not found !\n{e}"},
        )

    # Check if the connected user is the auction owner
    if request.user != listing.created_by:
        messages.error(request, "You do not have permission to close this auction.")
        return redirect("listing", id=id)

    # close the auction if it's still active
    if listing.is_active:
        listing.is_active = False
        listing.save()
        messages.success(request, "The auction has been successfully closed.")
    else:
        messages.info(request, "The auction is already closed.")

    return redirect("listing", id=id)


@login_required
def listing_watchlist_view(request, id):
    try:
        listing = get_object_or_404(Listing, id=id)
    except Exception as e:
        return (
            render(request),
            "auctions/error.html",
            {"code": 404, "message": f"Listing with id {id} not found !\n{e}"},
        )

    # check if the auction is active
    if not listing.is_active:
        messages.info(
            request, "The auction is closed. You can't add it to your watchlist."
        )
        return redirect("listing", id=id)

    # get or create the watchlist
    watchlist, _ = Watchlist.objects.get_or_create(user=request.user)

    # add or remove the listing to the watchlist user
    if listing in watchlist.listings.all():
        watchlist.listings.remove(listing)
        messages.success(request, "The listing has been removed from your watchlist.")
    else:
        watchlist.listings.add(listing)
        messages.success(request, "The listing has been added to your watchlist.")

    return redirect("listing", id=id)


def categories_view(request):
    try:
        categories = Category.objects.all()
    except Exception as e:
        return render(
            request,
            "auctions/error.html",
            {"code": 400, "message": f"Error loading the categories"},
        )

    return render(request, "auctions/categories.html", {"categories": categories})


def category_view(request, id):
    try:
        category = get_object_or_404(Category, id=id)
        listings_category = category.listings.filter(is_active=True)
    except Exception as e:
        return render(
            request,
            "auctions/error.html",
            {"code": 404, "message": f"Category {id} not found\n {e}"},
        )

    return render(
        request,
        "auctions/category_listing.html",
        {"listings_category": listings_category, "category": category},
    )


@login_required
def watchlist_view(request):
    try:
        watchlist, _ = Watchlist.objects.get_or_create(user=request.user)
    except Exception as e:
        return render(
            request,
            "auctions/error.html",
            {"code": 404, "message": f"Watchlist not found\n {e}"},
        )

    return render(
        request,
        "auctions/watchlist_listing.html",
        {"listings": watchlist.listings.all()},
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
