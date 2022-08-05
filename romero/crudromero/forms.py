from django import forms
from .models import Paciente, Visita


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = '__all__'