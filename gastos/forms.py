from django import forms
from .models import Categoria, Gasto, Ingreso, Presupuesto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'color']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nombre de la categoría'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-color'}),
        }

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['descripcion', 'monto']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Descripción del gasto'}),
            'monto': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Monto', 'step': '0.01'}),
        }

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['descripcion', 'monto', 'fuente']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Descripción del ingreso'}),
            'monto': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Monto', 'step': '0.01'}),
            'fuente': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Fuente (ej. Salario, Negocio)'}),
        }

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['limite']
        widgets = {
            'limite': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Límite Mensual', 'step': '0.01'}),
        }
