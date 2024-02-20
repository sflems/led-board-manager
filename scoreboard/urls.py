from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("", login_required(views.SettingsList.as_view()), name="profiles_list"), 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("profiles/", login_required(views.SettingsList.as_view()), name="profiles_list"), 
    path("profiles/active", views.active_profile, name="active_profile"), 
    path("profiles/create", views.profiles_create, name="create"),
    path("profiles/create/<str:board>", views.profiles_create, name="create"),
    path("profiles/<int:id>", views.profiles, name="profiles"),
    path("command", views.command, name="command_pi"),
    path("resources/", views.resource_monitor, name="resources"),
]