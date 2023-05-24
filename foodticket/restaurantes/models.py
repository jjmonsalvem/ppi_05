from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Restaurante(models.Model):
    nombre = models.CharField(max_length=100)
    NIT = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    tipo = models.CharField(max_length=100, blank=True)

    # Cada restaurante tiene un usuario asociado
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class RestauranteUsuario(models.Model):
    nombre = models.CharField(max_length=100)
    NIT = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    tipo = models.CharField(max_length=100, blank=True)

    # Cada restaurante tiene un usuario asociado
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class TiqueteraVenta(models.Model):
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    id_restaurante = models.ForeignKey(RestauranteUsuario, on_delete=models.CASCADE)