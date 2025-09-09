from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings",
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def highest_bid(self):
        return self.bids.order_by("-amount").first()
    
    def current_price(self):
        highest_bid = self.highest_bid()
        return highest_bid.amount if highest_bid else self.starting_bid

    def winner(self, user):
        highest_bid = self.bids.order_by("-amount").first()
        return not self.is_active and highest_bid and highest_bid.bidder == user


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username}: {self.amount} on {self.listing.title}"


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.listing.title}"


class Watchlist(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="watchlist"
    )
    listings = models.ManyToManyField(
        Listing, related_name="watchlisted_by", blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Watchlist"
