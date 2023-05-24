from django.contrib import admin
from django.urls import path
from . import views

app_name = "menus"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("crear/", views.crear_menu, name="crear_menu"),
    path("<int:menu_id>/eliminar", views.eliminar_menu, name="eliminar_menu"),
    path("<int:menu_id>/editar", views.editar_menu, name="editar_menu"),
] 