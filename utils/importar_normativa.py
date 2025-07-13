# utils/importar_normativa.py
import json
from app.models import Normativa, Estudio

def importar_desde_json(path):
    with open(path, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
        for item in datos:
            estudio, _ = Estudio.objects.get_or_create(nombre=item['estudio'])
            Normativa.objects.create(
                estudio=estudio,
                sexo=item['sexo'],
                edad_min=item['edad_min'],
                edad_max=item['edad_max'],
                anios_estudio_min=item.get('anios_estudio_min'),
                anios_estudio_max=item.get('anios_estudio_max'),
                media=item['media'],
                desviacion=item['desviacion']
            )
