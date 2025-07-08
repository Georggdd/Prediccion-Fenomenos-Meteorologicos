import requests
import json
import time
import os

API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJnZW9yZ2lhbmFkdW1pdHJ1ODRAZ21haWwuY29tIiwianRpIjoiYTE0ZjQyN2YtNmMwMS00NzMzLTkyNzQtNDY4YTRmYjQ0MmM2IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NTAzNTkwOTcsInVzZXJJZCI6ImExNGY0MjdmLTZjMDEtNDczMy05Mjc0LTQ2OGE0ZmI0NDJjNiIsInJvbGUiOiIifQ.KoH2IdjHqoudkn8QNlI7tsFZjkIWQIFffNwvh22YWzk'

# Solo las primeras 5 estaciones ordenadas alfabéticamente por nombre
ESTACIONES = [
     ("7275C", "Yecla"),
    ("7002Y", "Águilas")
]

def obtener_url_datos(anio_ini, anio_fin, estacion):
    url = f'https://opendata.aemet.es/opendata/api/valores/climatologicos/mensualesanuales/datos/anioini/{anio_ini}/aniofin/{anio_fin}/estacion/{estacion}'
    headers = {'api_key': API_KEY}
    print(f'📡 Solicitando URL de descarga para {estacion} en: {url}')
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('datos')
    except Exception as e:
        registrar_error(f'Error obteniendo URL para estación {estacion} ({anio_ini}-{anio_fin}): {e}')
        return None

def descargar_datos(url):
    print(f'⬇️ Descargando datos desde: {url}')
    for intento in range(3):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'⚠️ Intento {intento + 1} fallido: {e}')
            time.sleep(2 ** intento)  # espera exponencial
    registrar_error(f'❌ Fallo en la descarga de datos desde {url} después de 3 intentos.')
    return []

def registrar_error(mensaje):
    with open('errores_descarga.log', 'a', encoding='utf-8') as log:
        log.write(mensaje + '\n')
    print(mensaje)

if __name__ == '__main__':
    inicio = 2015
    fin = 2024
    rango_max = 3

    for codigo, nombre in ESTACIONES:
        nombre_archivo = f'{codigo}_{nombre.replace("/", "_").replace(",", "").replace(" ", "_")}_anuales_2015_2024.json'

        if os.path.exists(nombre_archivo):
            print(f'📁 Ya existe el archivo: {nombre_archivo}. Se omite la descarga.')
            continue

        datos_anuales = []
        print(f'\n📥 Descargando datos anuales para estación {codigo} - {nombre}...')

        for anio_ini in range(inicio, fin + 1, rango_max):
            anio_fin = min(anio_ini + rango_max - 1, fin)
            url_datos = obtener_url_datos(anio_ini, anio_fin, codigo)
            if not url_datos:
                continue
            datos = descargar_datos(url_datos)

            for registro in datos:
                fecha = registro.get('fecha', '')
                if fecha.endswith('-13'):
                    registro['nombre_estacion'] = nombre
                    datos_anuales.append(registro)

            time.sleep(1.5)  # Evita saturar el servidor

        if datos_anuales:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos_anuales, f, ensure_ascii=False, indent=2)
            print(f'✅ Archivo guardado: {nombre_archivo}')
        else:
            registrar_error(f'❌ No se obtuvieron datos válidos para {codigo} - {nombre}')
