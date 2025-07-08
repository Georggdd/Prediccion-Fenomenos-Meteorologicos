import requests
import datetime
import time
import os
import json

# CONFIGURACIÓN
API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJnZW9yZ2lhbmFkdW1pdHJ1ODRAZ21haWwuY29tIiwianRpIjoiYTE0ZjQyN2YtNmMwMS00NzMzLTkyNzQtNDY4YTRmYjQ0MmM2IiwiaXNzIjoiQUVNRVQiLCJpYXQiOjE3NTAzNTkwOTcsInVzZXJJZCI6ImExNGY0MjdmLTZjMDEtNDczMy05Mjc0LTQ2OGE0ZmI0NDJjNiIsInJvbGUiOiIifQ.KoH2IdjHqoudkn8QNlI7tsFZjkIWQIFffNwvh22YWzk'
start_year = 2015
end_year = 2025

# Lista de estaciones: (código, nombre)
estaciones = [
    ("7121A", "Calasparra"),
    ("7119B", "Caravaca de la Cruz"),
    ("7195X", "Caravaca de la Cruz, Los Royos"),
    ("7012C", "Cartagena"),
    ("7012D", "Cartagena"),
    ("7019X", "Cartagena/Salinas Cabo de Palos"),
    ("7145D", "Cieza"),
    ("7023X", "Fuente Alamo de Murcia"),
    ("7138B", "Jumilla"),
    ("7209", "Lorca"),
    ("7203A", "Lorca, Zarcilla de Ramos"),
    ("7007Y", "Mazarrón/Las Torres"),
    ("7237E", "Molina de Segura"),
    ("7080X", "Moratalla"),
    ("7172X", "Mula"),
    ("7178I", "Murcia"),
    ("7020C", "Murcia/Aeropuerto"),
    ("7211B", "Puerto Lumbreras"),
    ("7031", "San Javier Aeropuerto"),
    ("7031X", "San Javier Aeropuerto"),
    ("7026X", "Torre Pacheco"),
    ("7218Y", "Totana"),
    ("7275C", "Yecla"),
    ("7002Y", "Águilas"),
    ("7250C", "Abanilla"),
    ("7228", "Alcantarilla"),
    ("7227X", "Alhama de Murcia"),
    ("7158X", "Archena"),
    ("7127X", "Bullas"),
]

# Crear carpeta de salida
os.makedirs("datos_estaciones", exist_ok=True)

def generar_periodos(inicio, fin):
    periodos = []
    actual = inicio
    while actual < fin:
        siguiente = actual + datetime.timedelta(days=182)
        if siguiente > fin:
            siguiente = fin
        periodos.append((actual, siguiente))
        actual = siguiente + datetime.timedelta(days=1)
    return periodos

def descargar_periodo(station_id, nombre_estacion, fecha_ini, fecha_fin, i, acumulador, intentos=3):
    print(f"📡 {nombre_estacion} - Periodo {i}: {fecha_ini} → {fecha_fin}")
    url_peticion = f"https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini.strftime('%Y-%m-%d')}T00%3A00%3A00UTC/fechafin/{fecha_fin.strftime('%Y-%m-%d')}T23%3A59%3A59UTC/estacion/{station_id}"
    headers = {"api_key": API_KEY}

    for intento in range(1, intentos + 1):
        try:
            r = requests.get(url_peticion, headers=headers, timeout=20)
            if r.status_code != 200:
                raise Exception(f"❌ Error en la solicitud: {r.status_code} - {r.text}")

            datos_url = r.json().get('datos')
            if not datos_url:
                raise Exception("❌ No se encontró la URL de datos")

            r_datos = requests.get(datos_url, timeout=30)
            if r_datos.status_code != 200:
                raise Exception(f"❌ Error al descargar datos: {r_datos.status_code} - {r_datos.text}")

            datos = r_datos.json()
            acumulador.extend(datos)
            print(f"✔️  {len(datos)} registros añadidos\n")
            time.sleep(1)
            return

        except Exception as e:
            print(f"⚠️  Intento {intento} fallido: {e}")
            if intento < intentos:
                print("⏳ Reintentando en 5 segundos...\n")
                time.sleep(5)
            else:
                print("❌ Falló tras varios intentos. Continuando...\n")

# Ejecutar para todas las estaciones
inicio = datetime.date(start_year, 1, 1)
fin = datetime.date(end_year, 6, 30)
periodos = generar_periodos(inicio, fin)

for station_id, nombre_estacion in estaciones:
    print(f"\n==============================")
    print(f"🌍 Descargando datos de {nombre_estacion} ({station_id})")
    print(f"==============================")
    
    todos_los_datos = []
    
    for i, (f_ini, f_fin) in enumerate(periodos, 1):
        descargar_periodo(station_id, nombre_estacion, f_ini, f_fin, i, todos_los_datos)

    nombre_archivo = f"{nombre_estacion.replace('/', '_').replace(',', '').replace(' ', '_')}_{station_id}.json"
    ruta_salida = os.path.join("datos_estaciones", nombre_archivo)

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(todos_los_datos, f, ensure_ascii=False, indent=2)

    print(f"✅ Archivo guardado: {ruta_salida} ({len(todos_los_datos)} registros)\n")
    time.sleep(2)  # Evitar saturar la API

print("\n✅ Descarga completada para todas las estaciones.")
