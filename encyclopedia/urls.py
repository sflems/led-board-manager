from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("edit", views.edit, name="edit"),
    path("<str:title>", views.entry, name="entry"),
    path("search", views.index, name="search")
]
