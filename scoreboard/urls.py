from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path("settings_create/", views.settings_create, name="settings_create"),
    path('settings_list/', views.SettingsList.as_view(), name="settings_list"),
]