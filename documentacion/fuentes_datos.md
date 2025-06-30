# Fuentes de datos

Listado y descripción de los datasets meteorológicos y ambientales usados en el proyecto.

- AEMET: descripción y tipos de datos.
- IGN: descripción.
- Copernicus Climate Change Service: descripción.
- Otros métodos (web scraping, APIs).

# Tipos de Datos

Los datos a recopilar incluirán variables meteorológicas y ambientales como:

- Temperatura
- Precipitaciones
- Velocidad y dirección del viento
- Humedad
- Presión atmosférica

# Formatos y Acceso

Los datos pueden estar disponibles en distintos formatos:

- CSV, JSON, XML
- APIs REST para descarga directa
- Portales web con datasets públicos

# Plan de Acción
- Explorar portales oficiales para identificar datasets relevantes.
- Descargar muestras para analizar su estructura y calidad.
- Crear scripts en Python para automatizar la descarga de datos vía API o web scraping.
- Almacenar los datos en la carpeta /data del proyecto para su posterior procesamiento.

# Descarga de datos desde AEMET
Para usar la API de AEMET necesitas solicitar una clave (API key) gratuita en su web:
https://opendata.aemet.es/centrodedescargas/altaUsuario
Esta API key se usará para crear un script para la descarga de datos diarios de temperatura