from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

from  restaurantes.models import RestauranteUsuario

# Create your views here.

# Para crear la primera vista del home
class IndexView(generic.TemplateView):
    template_name = "home/index.html"


# Para crear la vista de registro
def registrarse(request):
    """Esta view se encarga de registrar un usuario y un restaurante asociado a ese usuario"""

    if request.method == "GET":
        return render(request, "home/registrarse.html")
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Creamos el usuario
                username = request.POST["username"]
                password = request.POST["password1"]
                email = request.POST["correo"]
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                # Logeamos al usuario creando la sesión
                login(request, user)

                # Creamos el restaurante de ese usuario
                nombre_restaurante = request.POST["nombre_restaurante"]
                nit_restaurante = request.POST["nit_restaurante"]
                direccion_restaurante = request.POST["direccion_restaurante"]
                telefono_restaurante = request.POST["telefono_restaurante"]
                tipo_restaurante = request.POST["tipo_restaurante"]
                restaurante = RestauranteUsuario.objects.create(nombre=nombre_restaurante, NIT=nit_restaurante, direccion=direccion_restaurante, telefono=telefono_restaurante, tipo=tipo_restaurante, usuario=user)
                restaurante.save()
                return redirect("restaurantes:index")

            except IntegrityError:
                return render(request, "home/registrarse.html", {"error": "El nombre de usuario ya existe"})
        else:
            return render(request, "home/registrarse.html", {"error": "Las contraseñas no coinciden"})


def cerrar_sesion(request):
    """Esta view se encarga de cerrar la sesión del usuario y redireccionar a la página de inicio"""
    logout(request)
    return redirect("home:index")

def tratamiento_de_datos(request):
    """politica de tratamiento de datos"""
    return render(request, "home/tratamiento_datos.html")


def iniciar_sesion(request):
    """Esta view se encarga de iniciar la sesión del usuario y redireccionar a la página de inicio"""
    if request.method == "GET":
        return render(request, "home/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Comprobamos si el usuario existe, o sea si el usuario y la contraseña son correctos
        if user is not None:
            login(request, user)
            return redirect("restaurantes:index")
        else:
            return render(request, "home/login.html", {"error": "El usuario o la contraseña son incorrectos"})

'''


def registrarse(request):
Esta vista se encarga de registrar un usuario y un restaurante asociado a ese usuario"""

    if request.method == "GET":
        return render(request, "home/registrarse.html")
    else:
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.POST.get("correo")
        nombre_restaurante = request.POST.get("nombre_restaurante")
        nit_restaurante = request.POST.get("nit_restaurante")
        direccion_restaurante = request.POST.get("direccion_restaurante")
        telefono_restaurante = request.POST.get("telefono_restaurante")
        tipo_restaurante = request.POST.get("tipo_restaurante")

        if password1 == password2:
            try:
                # Creamos el usuario
                user = User.objects.create_user(username=username, password=password1, email=email)

                # Logeamos al usuario creando la sesión
                # login(request, user)  # Si deseas iniciar sesión automáticamente

                # Creamos el restaurante de ese usuario
                restaurante = RestauranteUsuario.objects.create(
                    nombre=nombre_restaurante,
                    NIT=nit_restaurante,
                    direccion=direccion_restaurante,
                    telefono=telefono_restaurante,
                    tipo=tipo_restaurante,
                    usuario=user
                )

                return redirect("restaurantes:index")

            except IntegrityError:
                return render(request, "home/registrarse.html", {"error": "El nombre de usuario ya existe"})

        else:
            return render(request, "home/registrarse.html", {"error": "Las contraseñas no coinciden"})
'''
