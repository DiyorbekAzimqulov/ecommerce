from django.core.exceptions import ViewDoesNotExist
from django.urls import path

from . import views


app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create-listing/", views.create_listing, name='create-listing'),
    path("listings/<int:id>", views.listing_detail, name='listing-detail'),
    path("categories/", views.categories, name='categories'),
    path("watchlist/", views.watchlist, name='watchlist'),
    path("close-listing/", views.close_listing, name='close-listing'),
    path("inactive/", views.inactive, name='inactive'),
    path("comment/", views.comment, name="comment")
]
