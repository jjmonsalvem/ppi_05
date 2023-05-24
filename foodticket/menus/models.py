from django.db import models
from restaurantes.models import RestauranteUsuario
import os
from django.core.exceptions import ValidationError

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # Obtener la extensión del archivo
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('El archivo debe ser un PNG, JPG o JPEG')
    
# Create your models here.
class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='menu_imagenes', blank=True, null=True, validators=[validate_image_extension])
    lunes = models.BooleanField(default=False)
    martes = models.BooleanField(default=False)
    miercoles = models.BooleanField(default=False)
    jueves = models.BooleanField(default=False)
    viernes = models.BooleanField(default=False)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)

    id_restaurante = models.ForeignKey(RestauranteUsuario, on_delete=models.CASCADE)



