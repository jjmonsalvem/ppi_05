from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import FormularioVentaTiquetera,FormularioVentaAlmuerzo, ClienteForm
from .models import Cliente, Tiquetera
from restaurantes.models import RestauranteUsuario, TiqueteraVenta
from pedidos.models import Pedido, MenuPedido
from menus.models import Menu

# Create your views here.

#TODO: Agregar validaciones de login

def index(request):
    return render(request, "clientes/index.html")


@login_required
def venta(request):

    formulario = FormularioVentaTiquetera()
    restaurante = RestauranteUsuario.objects.get(usuario=request.user)
    tiqueteras_restaurante = TiqueteraVenta.objects.filter(id_restaurante=restaurante)

    if request.method == 'POST':

        formulario = FormularioVentaTiquetera(data=request.POST)
        restaurante = RestauranteUsuario.objects.get(usuario=request.user)

        if formulario.is_valid():
            nombre = request.POST.get("nombre")
            cedula = request.POST.get("cedula")

        # Se guarda la tiquetaera seleccionada
        tiquetera_venta = TiqueteraVenta.objects.get(id=request.POST.get("tiquetera_select"))
        cantidad_tiquetes = tiquetera_venta.cantidad
        # Si el cliente no existe debe crearse
        try:
            cliente = Cliente.objects.create(nombre=nombre, cedula=cedula)
            tiquetera = Tiquetera.objects.create(cantidad=cantidad_tiquetes, id_restaurante=restaurante, id_cliente=cliente)

            # Se debe guardar el cliente y la tiquetera
            cliente.save()
            tiquetera.save()

        # Si el cliente ya existe se debe recuperar para asiganrle la tiquetera
        except IntegrityError:
            cliente = Cliente.objects.get(cedula=cedula)

            tiquetera = Tiquetera.objects.create(cantidad=cantidad_tiquetes, id_restaurante=restaurante, id_cliente=cliente)

            # Se debe guardar la tiquetera

            tiquetera.save()

        return redirect("clientes:index")
    else:
        return render(request, "clientes/venta.html", {
            "formulario_venta": formulario,
            "tiqueteras": tiqueteras_restaurante
            })


@login_required
def compra(request):

    formulario = FormularioVentaAlmuerzo()
    restaurante = RestauranteUsuario.objects.get(usuario=request.user)

    if request.method == 'POST':

        try:
            cliente = Cliente.objects.get(cedula=request.POST.get("cedula"))
            tiqueteras = Tiquetera.objects.filter(id_cliente=cliente, id_restaurante = restaurante)
            if tiqueteras.count() == 0:
                return render(request, "clientes/compra.html",
                            {"error": "El cliente no tiene tiqueteras",
                            "formulario_compra": formulario}
                            )
            return redirect("clientes:seleccionar_tiquetera", cliente_id=cliente.id)

        except ObjectDoesNotExist:
            return render(request, "clientes/compra.html",
                            {"error": "El cliente no tiene tiqueteras",
                            "formulario_compra": formulario}
                            )

    else:
        return render(request, "clientes/compra.html", {"formulario_compra": formulario})


# TODO: Si no se seleccionan menus igual se descuenta la tiquetera, se debe solucionar esto tal vez guardando todo en una misma
# View y en esta solo hacer la verificación si hay tiquetes suficientes o no
@login_required
def seleccionar_tiquetera(request, cliente_id):

    restaurante = RestauranteUsuario.objects.get(usuario=request.user)
    tiqueteras = Tiquetera.objects.filter(id_restaurante = restaurante, id_cliente = cliente_id)
    cliente = Cliente.objects.get(id=cliente_id)

    if request.method == 'POST':
            tiquetera = Tiquetera.objects.get(pk=request.POST.get("tiquetera_select"), id_restaurante = restaurante, id_cliente = cliente)

            # Se debe validar que la cantidad de tiquetes sea suficiente
            if tiquetera.cantidad - tiquetera.redimidos >= int(request.POST.get("cantidad")):
                tiquetera.redimidos += int(request.POST.get("cantidad"))

                # Si se iguala la cantidad de tiquetes a la cantidad de tiquetes redimidos se debe eliminar la tiquetera
                if tiquetera.cantidad == tiquetera.redimidos:
                    tiquetera.delete()
                else:
                    tiquetera.save()
            else:
                return render(request, "clientes/seleccionTiquetera.html",
                            {"error": "No hay suficientes tiquetes para realizar la compra",
                            "tiqueteras": tiqueteras, "cliente": cliente}
                            )

            return render(request, "clientes/seleccionMenu.html",{
                "cliente": cliente, "menus": restaurante.menu_set.all(),
                "cantidad": [i for i in range(int(request.POST.get("cantidad")))]
                })
    else:
        return render(request, "clientes/seleccionTiquetera.html",
                        {"tiqueteras": tiqueteras, "cliente": cliente})


@login_required
def seleccionar_menu(request, cliente_id):

    restaurante = RestauranteUsuario.objects.get(usuario=request.user)
    cliente = Cliente.objects.get(id=cliente_id)
    menus = restaurante.menu_set.all()

    if request.method == 'POST':
        menus_seleccionados = dict(request.POST.items())
        menus_seleccionados.pop("csrfmiddlewaretoken")

        pedido = Pedido.objects.create(id_restaurante=restaurante, fecha=timezone.now(), id_cliente=cliente)

        # Se cuentas las veces que se pide un menu
        cantidad = {}
        for i, menu_id in menus_seleccionados.items():
            cantidad[menu_id] = cantidad.get(menu_id, 0) + 1

        # Se añaden los menus al pedido y su cantidad
        for i in menus_seleccionados:
            menu = Menu.objects.get(pk=menus_seleccionados[i])
            pedido.menus_comprados.add(menu, through_defaults={'cantidad': cantidad[str(menus_seleccionados[i])]})

        pedido.save()

        return redirect("clientes:index")
    else:
        return render(request, "clientes/seleccionMenu.html",
                        {"menus": menus, "cliente": cliente})


# TODO: Al momento de vender tiqueteras sería conveniente vernder una cantidad especifica y no x cantidad
# Tal vez reemplazar este modo de compra perimitiendo seleccionar la tiquetera previamente creada por el restaurante
# TODO: Si se implementa lo anterior crear la view para crear tiqueteras
# TODO: Implementar la funcionalidad para que el cliente pueda ver sus tiqueteras
# TODO: Implementar la funcionalidad para dar almuerzos gratis por una cantidad de tiqueteras redimidas si el restaurante lo desea

def informacion_cliente(request, cliente_id):

    formulario = FormularioVentaAlmuerzo()
    restaurante = RestauranteUsuario.objects.get(usuario=request.user)

    if request.method == 'POST':

        try:
            cliente = Cliente.objects.get(cedula=request.POST.get("cedula"))
            tiqueteras = Tiquetera.objects.filter(id_cliente=cliente, id_restaurante = restaurante)
            if tiqueteras.count() == 0:
                return render(request, "clientes/compra.html",
                            {"error": "El cliente no tiene tiqueteras",
                            "formulario_compra": formulario}
                            )
            return redirect("clientes:seleccionar_tiquetera", cliente_id=cliente.id)

        except ObjectDoesNotExist:
            return render(request, "clientes/compra.html",
                            {"error": "El cliente no tiene tiqueteras",
                            "formulario_compra": formulario}
                            )

    else:
        return render(request, "clientes/compra.html", {"formulario_compra": formulario})







    """restaurante = RestauranteUsuario.objects.get(usuario=request.user)
    tiqueteras = Tiquetera.objects.filter(id_restaurante = restaurante, id_cliente = cliente_id)
    cliente = Cliente.objects.get(id=cliente_id)

    if request.method == 'POST':
            tiquetera = Tiquetera.objects.get(pk=request.POST.get("tiquetera_select"), id_restaurante = restaurante, id_cliente = cliente)

            # Se debe validar que la cantidad de tiquetes sea suficiente
            if tiquetera.cantidad - tiquetera.redimidos >= int(request.POST.get("cantidad")):
                tiquetera.redimidos += int(request.POST.get("cantidad"))

                # Si se iguala la cantidad de tiquetes a la cantidad de tiquetes redimidos se debe eliminar la tiquetera
                if tiquetera.cantidad == tiquetera.redimidos:
                    tiquetera.delete()
                else:
                    tiquetera.save()
            else:
                return render(request, "clientes/seleccionTiquetera.html",
                            {"error": "No hay suficientes tiquetes para realizar la compra",
                            "tiqueteras": tiqueteras, "cliente": cliente}
                            )

            return render(request, "clientes/seleccionMenu.html",{
                "cliente": cliente, "menus": restaurante.menu_set.all(),
                "cantidad": [i for i in range(int(request.POST.get("cantidad")))]
                })
    else:
        return render(request, "clientes/seleccionTiquetera.html",
                        {"tiqueteras": tiqueteras, "cliente": cliente})"""