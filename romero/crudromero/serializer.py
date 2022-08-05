from rest_framework import serializers
from .models import Paciente, Visita


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = '__all__'
