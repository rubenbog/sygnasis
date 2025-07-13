from django.core.management.base import BaseCommand
from app.models import Normativa

class Command(BaseCommand):
    help = 'Verifica normativas con media o desviación inválidas'

    def handle(self, *args, **kwargs):
        errores = Normativa.objects.filter(
            media__isnull=True
        ) | Normativa.objects.filter(
            desviacion__isnull=True
        ) | Normativa.objects.filter(
            desviacion=0
        )

        if not errores.exists():
            self.stdout.write(self.style.SUCCESS("✅ Todas las normativas están correctamente cargadas."))
        else:
            self.stdout.write(self.style.WARNING("⚠ Normativas con errores encontrados:\n"))
            for n in errores:
                self.stdout.write(
                    f"- Estudio: {n.estudio.nombre}, Sexo: {n.sexo}, Edad: {n.edad_min}-{n.edad_max}, "
                    f"Años estudio: {n.anios_estudio_min}-{n.anios_estudio_max}, "
                    f"Media: {n.media}, Desviación: {n.desviacion}"
                )
