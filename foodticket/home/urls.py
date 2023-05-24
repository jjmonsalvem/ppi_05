from django.contrib import admin
from django.urls import path

from . import views

app_name = "home"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("registrarse/", views.registrarse, name="registrarse"),
    path("cerrar_sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("login/", views.iniciar_sesion, name="login"),
]