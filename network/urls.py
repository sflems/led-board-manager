
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.PostCreateView.as_view(), name="post_create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # API Routes
    path("views/<str:view>", views.view, name="view"),

    # TODO: Implement Post Create, Update, & Delete API

]
