from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from .models import Menu
from  restaurantes.models import RestauranteUsuario
from .forms import MenuForm
# Create your views here.

class IndexView(generic.ListView):
    """
    View principal de los menús del restaurante
    
    pasa como contexto los menus del restaurante del usuario que está con la sesión iniciada
    """
    template_name = "menus/index.html"

    context_object_name = "menus_restaurante"

    def get_queryset(self):
        # Si el usuario está autenticado, devolvemos los menús del restaurante del usuario
        if self.request.user.is_authenticated:
            return Menu.objects.filter(id_restaurante__usuario=self.request.user)
    

# TODO: Implementar la lógica para permitir añadir una imagen al menú
@login_required
def crear_menu(request):
    """Crea un menú para el restaurante del usuario que está con la sesión iniciada"""
    if request.method == "GET":
        return render(request, "menus/crear_menu.html", {
            "form": MenuForm
        })
    else:
        try:
            # Llenamos el formulario con los datos ya creado con los datos del POST y los archivos subidos
            form = MenuForm(request.POST, request.FILES)

            # Guardamos los datos como un menu, pero no guardamos en la DB
            menu = form.save(commit=False)
            
            # Asignamos el restaurante del usuario a la variable restaurante
            restaurante = RestauranteUsuario.objects.get(usuario=request.user)

            # Asignamos el restaurante del usuario al menú
            menu.id_restaurante = restaurante

            # Comprobamos si el checkbox de diario está marcado para marcar todos los días
            try:
                if request.POST["diario"] == "on":
                    menu.lunes = True
                    menu.martes = True
                    menu.miercoles = True
                    menu.jueves = True
                    menu.viernes = True
                    menu.sabado = True
                    menu.domingo = True
            except:
                pass
            
            # Guardamos el menú en la base de datos
            menu.save()

            # Redirigimos al usuario a la página de menus
            return redirect("menus:index")
        except IntegrityError:
            return render(request, "menus/crear_menu.html", {
                "error": "Menú ya creado"
            })
        except ValueError:
            return render(request, "menus/crear_menu.html", {
                "error": "Formato no admitido",
                "form": MenuForm
            })


@login_required
def eliminar_menu(request, menu_id):
    """Elimina el menú con el id pasado por parámetro"""
    # Buscamos el menú con el id pasado por parámetro
    menu = get_object_or_404(Menu, id=menu_id)

    # Eliminamos el menú
    menu.delete()

    # Redirigimos al usuario a la página de menus
    return redirect("menus:index")


@login_required
def editar_menu(request, menu_id):
    """Edita el menú con el id pasado por parámetro"""
    # Buscamos el menú con el id pasado por parámetro
    menu = get_object_or_404(Menu, id=menu_id)

    if request.method == "GET":
        return render(request, "menus/editar_menu.html", {
            "form": MenuForm(instance=menu),
            "menu": menu
        })
    else:
        try:
            # Llenamos el formulario con los datos ya creado con los datos del POST
            form = MenuForm(request.POST, instance=menu)

            # Actualizamos el menú en la base de datos
            form.save()

            # Redirigimos al usuario a la página de menus
            return redirect("menus:index")
        except IntegrityError:
            return render(request, "menus/editar_menu.html", {
                "error": "Menú ya creado"
            })