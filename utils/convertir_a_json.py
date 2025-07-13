import csv
import json
import sys

if len(sys.argv) < 2:
    print("Debes indicar el nombre del archivo de entrada.")
    print("Ejemplo: python convertir_a_json.py archivo.txt")
    sys.exit(1)

entrada = sys.argv[1]  # nombre del archivo pasado por consola
salida = "normativas.json"
cont=0;
normativas = []

with open(entrada, encoding="latin1") as archivo_csv:
    lector = csv.reader(archivo_csv, delimiter=';')
    for fila in lector:
        if len(fila) < 8:
            continue  # saltear líneas incompletas
        estudio, sexo, edad_min, edad_max, edu_min, edu_max, media, desvio = fila
        normativa = {
            "estudio": estudio.strip(),
            "sexo": sexo.strip(),
            "edad_min": int(edad_min),
            "edad_max": int(edad_max),
            "anios_estudio_min": int(edu_min),
            "anios_estudio_max": int(edu_max),
            "media": float(media.replace(',', '.')),
            "desviacion": float(desvio.replace(',', '.'))
        }
        normativas.append(normativa)
        cont=cont+1

with open(salida, "w", encoding="utf-8") as f_json:
    json.dump(normativas, f_json, indent=2, ensure_ascii=False)

print(f" {cont} lineas cargadas en el archivo, con éxito en {salida}")
