from django.contrib import admin
from django.urls import path

from . import views

app_name = "restaurantes"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("crear/tiquetera/", views.crear_tiquetera, name="crear_tiquetera"),
]