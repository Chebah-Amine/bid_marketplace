from django import forms
from .models import Category


class BidForm(forms.Form):
    bid = forms.DecimalField(
        max_digits=10, decimal_places=2, label="Bid ($):", min_value=0.01
    )


class CommentForm(forms.Form):
    comment = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Add a comment..."}),
        label="Comment",
        # Django specified keys
        error_messages={
            "required": "Comment must not be empty.",
            "max_length": "Comment must contain less than 500 characters.",
        },
    )


class ListingForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label="Title",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter the title"}
        ),
        error_messages={
            "required": "Title is required.",
            "max_length": "Title must be between 1 and 100 characters.",
        },
    )
    description = forms.CharField(
        max_length=500,
        label="Description",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Describe your listing"}
        ),
        error_messages={
            "required": "Description is required.",
            "max_length": "Description must be between 1 and 500 characters.",
        },
    )
    starting_bid = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Starting Bid ($)",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Enter starting bid"}
        ),
        min_value=0.01,
        error_messages={
            "required": "Starting bid is required.",
            "min_value": "Starting bid must be greater than $0.",
        },
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
