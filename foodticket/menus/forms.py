from django import forms
from .models import Menu

class MenuForm(forms.ModelForm):
    class Meta:
        # Modelo en el cual estará basado el formulario
        model = Menu
        # Campos que se mostrarán en el formulario
        fields = ["nombre", "descripcion", "imagen", "lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control mt-1", "required": True}),
            "descripcion": forms.Textarea(attrs={"class": "form-control mt-1", "required": True}),
            "imagen": forms.FileInput(attrs={"class": "form-control mt-1", "required": True}),
            "lunes": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "martes": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "miercoles": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "jueves": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "viernes": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "sabado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "domingo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "imagen": "Imagen del menú: *.png",
        }