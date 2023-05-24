from django import forms
from .models import Cliente, Tiquetera
class FormularioVentaTiquetera(forms.Form):
    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={"class": "form-control"}))
    cedula = forms.CharField(label="Cedula", widget=forms.TextInput(attrs={"class": "form-control", "required": True}))
    

class FormularioVentaAlmuerzo(forms.Form):
    cedula = forms.CharField(label="Cedula", widget=forms.TextInput(attrs={"class": "form-control", "required": True}))


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nombre", "cedula"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "cedula": forms.TextInput(attrs={"class": "form-control", "required": True}),
        }