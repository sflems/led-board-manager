from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path('settings_list/', views.SettingsList.as_view(), name="settings_list"), 
    path("settings_create/", views.settings_create, name="create"),
    path('settings_activate/<int:id>', views.settings_activate, name="activate"),
]