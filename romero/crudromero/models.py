from django.db import models


class Paciente(models.Model):
    fecha = models.CharField(max_length=10)
    hora = models.CharField(max_length=5)
    apellido = models.CharField(max_length=50, blank=True)
    nombre = models.CharField(max_length=50)
    edad = models.IntegerField(null=True, blank=True)
    dni = models.CharField(max_length=8)
    sexo = models.CharField(max_length=20, blank=True)
    domicilio = models.CharField(max_length=150, blank=True)
    telefono = models.IntegerField(null=True, blank=True)
    barrio = models.CharField(max_length=100, blank=True)
    region_satinaria = models.CharField(max_length=100, blank=True)
    motivo_consulta = models.CharField(max_length=50, blank=True)
    evaluacion = models.CharField(max_length=300, blank=True)
    tratamiento_psicofarm = models.CharField(max_length=300, blank=True)
    internacion = models.CharField(max_length=12, blank=True)
    derivacion = models.CharField(max_length=2, blank=True)
    auxilio = models.CharField(max_length=100, blank=True)
    guardia_clinica = models.CharField(max_length=200, blank=True)
    intervencion = models.CharField(max_length=100, blank=True)
    profesionales = models.TextField()
