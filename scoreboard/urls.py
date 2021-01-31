from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),

    path('profiles/', views.SettingsList.as_view(), name="profiles_list"), 
    path("profiles/create", views.profiles_create, name="create"),
    path('profiles/<int:id>', views.profiles, name="profiles"),
]