
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    # API Routes
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("posts/create", views.CreatePost, name="create_post"),
    path("posts/<int:post_id>", views.UpdatePost, name="update_post"),

]
