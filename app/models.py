# Modelos para Paciente, Estudio, Resultado
# models.py
from django.db import models
from datetime import date 

class Paciente(models.Model):
    dni = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    años_educacion = models.IntegerField()
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='hijos_padre')
    madre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='hijos_madre')
    conyuge = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='conyuge_de')

    def edad(self):
        today = date.today()
        return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"
  

class Diagnostico(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    subtipo = models.CharField(max_length=100, blank=True, null=True)
    severidad = models.CharField(max_length=50, choices=[('Leve', 'Leve'), ('Moderado', 'Moderado'), ('Demencia', 'Demencia')])
    fecha = models.DateField(auto_now_add=True)

class Sintoma(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha = models.DateField(auto_now_add=True)

class Comorbilidad(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True, null=True)

class Medicacion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    dosis = models.CharField(max_length=100)
    indicaciones = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)

class Informe(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateField(auto_now_add=True)

class Estudio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    depende_educacion = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Normativa(models.Model):
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    edad_min = models.IntegerField()
    edad_max = models.IntegerField()
    anios_estudio_min = models.IntegerField(blank=True, null=True)
    anios_estudio_max = models.IntegerField(blank=True, null=True)
    media = models.FloatField()
    desviacion = models.FloatField()

    def __str__(self):
        return f"{self.estudio.nombre} | {self.edad_min}-{self.edad_max} años | {self.sexo} | {self.anios_estudio_min}-{self.anios_estudio_max} años estudio"


class Resultado(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE)
    puntaje_bruto = models.FloatField()
    media = models.FloatField()
    desviacion = models.FloatField()
    puntuacion_z = models.FloatField(blank=True, null=True)
    perfil_desempeno = models.CharField(max_length=20, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)

    def calcular_z(self):
        if self.media is not None and self.desviacion and self.desviacion != 0:
            return round((self.puntaje_bruto - self.media) / self.desviacion, 2)
        return None

    def clasificar_desempeno(self, z):
        if z is None:
            return "No calculado"
        if z < -2.5:
            return "Grave"
        elif z < -2.0:
            return "Moderado"
        elif z < -1.5:
            return "Leve"
        elif -1.5 <= z <= 1.5:
            return "Normal"
        elif z > 1.5:
            return "Superior"
        return "Desconocido"

    def save(self, *args, **kwargs):
        self.puntuacion_z = self.calcular_z()
        self.perfil_desempeno = self.clasificar_desempeno(self.puntuacion_z)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.paciente} - {self.estudio} Z={self.puntuacion_z}"


# Estructura de evaluación
# ------------------------
class DominioCognitivo(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Subtest(models.Model):
    nombre = models.CharField(max_length=100)
    dominio = models.ForeignKey(DominioCognitivo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.dominio})"


class ItemEvaluado(models.Model):
    nombre = models.CharField(max_length=100)
    subtest = models.ForeignKey(Subtest, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.subtest}"


