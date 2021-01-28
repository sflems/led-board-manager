from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("settings", views.settings_view, name="settings_view"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
]