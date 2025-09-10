from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.create_listing_view, name="create_listing"),
    path("listings/<int:id>", views.listing_view, name="listing"),
    path("listings/<int:id>/close", views.listing_close_view, name="close_listing"),
    path(
        "listings/<int:id>/watchlist",
        views.listing_watchlist_view,
        name="watchlist_listing",
    ),
    path("categories", views.categories_view, name="categories"),
    path("categories/<int:id>", views.category_view, name="category"),
    path("watchlist", views.watchlist_view, name="watchlist"),
]
