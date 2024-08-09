from django import forms
from .models import tarea


class tareaForma(forms.ModelForm):
    class Meta:
        model = tarea
        fields = ["titulo", "descripcion", "importante"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "titulo de la tarea"}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "descripcion de la tarea",
                }
            ),
            "importante": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
