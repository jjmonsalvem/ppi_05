from django.db import models
from django.utils import timezone
from restaurantes.models import RestauranteUsuario
from clientes.models import Cliente
from menus.models import Menu


# Create your models here.
class Pedido(models.Model):
    fecha = models.DateTimeField(default=timezone.now)

    id_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    id_restaurante = models.ForeignKey(RestauranteUsuario, on_delete=models.CASCADE)
    menus_comprados = models.ManyToManyField(Menu, through='MenuPedido')


class MenuPedido(models.Model):
    id_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    id_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)