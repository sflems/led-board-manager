from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("listing/create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.categories_index, name="categories_index"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/watchlist_add", views.watchlist_add, name="watchlist_add"),
    path("listing/<int:listing_id>/watchlist_remove", views.watchlist_remove, name="watchlist_remove"),
]
