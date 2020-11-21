from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("<str:title>", views.entry, name="entry")
]
