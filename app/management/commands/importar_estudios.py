import json
from django.core.management.base import BaseCommand
from app.models import Paciente, Estudio, Normativa, ResultadoEstudio

class Command(BaseCommand):
    help = 'Importa resultados de estudios desde un archivo JSON'

    def add_arguments(self, parser):
        parser.add_argument('ruta_json', type=str)

    def handle(self, *args, **kwargs):
        ruta_json = kwargs['ruta_json']

        with open(ruta_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        for entrada in datos:
            try:
                paciente = Paciente.objects.get(dni=entrada['dni'])
                estudio = Estudio.objects.get(nombre=entrada['estudio'])
                puntaje = float(entrada['puntaje_bruto'])

                normativa = Normativa.objects.filter(
                    estudio=estudio,
                    sexo=paciente.sexo,
                    edad_min__lte=paciente.edad,
                    edad_max__gte=paciente.edad,
                    educacion_min__lte=paciente.anios_estudio,
                    educacion_max__gte=paciente.anios_estudio
                ).first()

                if not normativa:
                    self.stdout.write(self.style.WARNING(
                        f"Sin normativa para {paciente.dni} - {estudio.nombre}"
                    ))
                    continue

                z = round((puntaje - normativa.media) / normativa.desviacion, 2)

                ResultadoEstudio.objects.create(
                    paciente=paciente,
                    estudio=estudio,
                    puntaje_bruto=puntaje,
                    media=normativa.media,
                    desviacion=normativa.desviacion,
                    puntuacion_z=z
                )

                self.stdout.write(self.style.SUCCESS(
                    f"{paciente.dni} - {estudio.nombre} -> Z = {z}"
                ))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error con {entrada}: {str(e)}"))
