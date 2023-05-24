from django import forms
from .models import TiqueteraVenta

class FormularioVentaTiquetera(forms.ModelForm):
    class Meta:
        model = TiqueteraVenta
        fields = ["cantidad", "precio"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "required": True}),
            "precio": forms.NumberInput(attrs={"class": "form-control", "required": True}),
        }
