from django import forms
from django.db import models
from .models import Medicacion

from .models import (
    Paciente,
    Resultado,
    Diagnostico,
    Sintoma,
    Comorbilidad,
    Informe,
    Medicacion,
    Estudio,
    Normativa,
)

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['dni', 'nombre', 'apellido', 'fecha_nacimiento', 'sexo', 'años_educacion']

class ResultadoForm(forms.ModelForm):
    class Meta:
        model = Resultado
        exclude = ['paciente']
        fields = ['paciente', 'estudio', 'puntaje_bruto']
        labels = {
            'estudio': 'Estudio aplicado',
            'puntaje_bruto': 'Puntaje obtenido',
        }
        widgets = {
            'estudio': forms.Select(attrs={'class': 'form-select'}),
            'puntaje_bruto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['tipo', 'subtipo', 'severidad']

class SintomaForm(forms.ModelForm):
    class Meta:
        model = Sintoma
        fields = ['descripcion']

class ComorbilidadForm(forms.ModelForm):
    class Meta:
        model = Comorbilidad
        fields = ['nombre', 'observaciones']

class InformeForm(forms.ModelForm):
    class Meta:
        model = Informe
        fields = ['contenido']

class MedicacionForm(forms.ModelForm):
    class Meta:
        model = Medicacion
        fields = ['nombre', 'dosis', 'indicaciones', 'fecha_inicio', 'fecha_fin']  # ❌ No incluir 'paciente'
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }


class EstudioForm(forms.ModelForm):
    class Meta:
        model = Estudio
        fields = ['nombre', 'descripcion', 'depende_educacion']       

class NormativaForm(forms.ModelForm):
    class Meta:
         model = Normativa  
         fields = '__all__'

class BuscarPacienteForm(forms.Form):
    dni = forms.CharField(label="Buscar por DNI", max_length=20)
    
  
class RelacionesForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['padre', 'madre', 'conyuge']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Excluir al mismo paciente en todas las relaciones
        if self.instance:
            self.fields['padre'].queryset = Paciente.objects.exclude(id=self.instance.id).filter(sexo='M')
            self.fields['madre'].queryset = Paciente.objects.exclude(id=self.instance.id).filter(sexo='F')
            self.fields['conyuge'].queryset = Paciente.objects.exclude(id=self.instance.id)
