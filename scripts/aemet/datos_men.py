import requests
import json
import time

API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJnZW9yZ2lhbmFkdW1pdHJ1ODRAZ21haWwuY29tIiwianRpIjoiYTE0ZjQyN2YtNmMwMS00NzMzLTkyNzQtNDY4YTRmYjQ0MmM2IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NTAzNTkwOTcsInVzZXJJZCI6ImExNGY0MjdmLTZjMDEtNDczMy05Mjc0LTQ2OGE0ZmI0NDJjNiIsInJvbGUiOiIifQ.KoH2IdjHqoudkn8QNlI7tsFZjkIWQIFffNwvh22YWzk'

ESTACIONES = [
     ("7026X", "Torre Pacheco"),
    ("7218Y", "Totana"),
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
    except requests.RequestException as e:
        print(f'❌ Error en obtener_url_datos: {e}')
        return None

def descargar_datos(url):
    headers = {'api_key': API_KEY}  # En caso de que lo requiera
    print(f'⬇️ Descargando datos desde: {url}')
    max_retries = 3
    for intento in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f'⚠️ Error en descargar_datos (intento {intento+1}/{max_retries}): {e}')
            time.sleep(5)
    print('❌ Falló la descarga después de varios intentos.')
    return None

if __name__ == '__main__':
    inicio = 2015
    fin = 2025
    rango_max = 2  # Puedes probar con intervalos más cortos para evitar caducidad URL

    for codigo, nombre in ESTACIONES:
        datos_mensuales = []
        print(f'\n📥 Descargando datos mensuales para estación {codigo} - {nombre}...')

        for anio_ini in range(inicio, fin + 1, rango_max):
            anio_fin = min(anio_ini + rango_max - 1, fin)
            url_datos = obtener_url_datos(anio_ini, anio_fin, codigo)
            if not url_datos:
                continue
            datos = descargar_datos(url_datos)
            if not datos:
                continue

            for registro in datos:
                fecha = registro.get('fecha', '')
                if not fecha.endswith('-13'):  # Solo meses (no anual)
                    registro['nombre_estacion'] = nombre
                    datos_mensuales.append(registro)

            time.sleep(3)  # Espera un poco más para evitar bloqueos

        nombre_archivo = f'{codigo}_{nombre.replace("/", "_").replace(",", "").replace(" ", "_")}_mensuales_2015_2025.json'
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_mensuales, f, ensure_ascii=False, indent=2)
        print(f'✅ Archivo guardado: {nombre_archivo}')
