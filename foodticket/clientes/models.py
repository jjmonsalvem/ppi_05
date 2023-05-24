from django.db import models
from restaurantes.models import RestauranteUsuario

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)


class Tiquetera(models.Model):
    cantidad = models.IntegerField(default=0)
    redimidos = models.IntegerField(default=0)
    id_restaurante = models.ForeignKey(RestauranteUsuario, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
