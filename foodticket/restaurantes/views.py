from django.shortcuts import render
from django.views import generic
from .forms import FormularioVentaTiquetera
from .models import RestauranteUsuario
# Create your views here.

# Para crear la primera vista del home
class IndexView(generic.TemplateView):
    template_name = "restaurantes/index.html"


def crear_tiquetera(request):
    form = FormularioVentaTiquetera()
    """Crea una tiquetera para el restaurante del usuario que está con la sesión iniciada"""
    if request.method == "GET":
        return render(request, "restaurantes/crear_tiquetera.html", {"form": form})
    else:
        try:
            # Llenamos el formulario con los datos ya creado con los datos del POST y los archivos subidos
            form = FormularioVentaTiquetera(request.POST)

            # Guardamos los datos como una tiquetera, pero no guardamos en la DB
            tiquetera = form.save(commit=False)
            tiquetera.id_restaurante = RestauranteUsuario.objects.get(usuario=request.user)
            tiquetera.save()
            return render(request, "restaurantes/index.html", {"form": form})
        except ValueError:
            return render(request, "restaurantes/crear_tiquetera.html", {
                "form": form,
                "error": "Error al crear la tiquetera"
                })