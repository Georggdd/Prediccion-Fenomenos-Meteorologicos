# Trabajo con Datos Climáticos de Copernicus: Desde la Descarga hasta la Visualización

1. Introducción
En este proyecto, se obtiene, procesa y visualiza información climática histórica para el periodo 2015-2025 utilizando datos satelitales y de reanálisis atmosférico del programa Copernicus Climate Data Store (CDS). La finalidad es analizar variables clave que afectan el clima local y desarrollar visualizaciones interactivas para facilitar su interpretación.

2. Tecnologías Empleadas
Python: Lenguaje principal para descarga, procesamiento y visualización.

cdsapi: Biblioteca oficial para acceder a la API de Copernicus Climate Data Store.

xarray: Manejo eficiente de datos multidimensionales NetCDF.

netCDF4: Biblioteca para lectura y escritura de archivos NetCDF.

Streamlit: Framework para crear aplicaciones web interactivas de visualización de datos.

Jupyter Notebook: Entorno para análisis exploratorio y visualización interactiva.

Matplotlib y Seaborn: Bibliotecas de visualización en Python para gráficos estáticos.

Pandas: Para manipulación y análisis de datos tabulares.

3. Obtención de Datos de Copernicus
3.1 Registro y configuración
Registrarse en el portal de Copernicus Climate Data Store.

Descargar e instalar el cliente cdsapi con pip install cdsapi.

Configurar credenciales (archivo .cdsapirc) para acceso autorizado a la API.

3.2 Elección de variables climáticas
Para un análisis climático completo se seleccionan variables relevantes que pueden afectar el clima local:

Variables atmosféricas:

Viento a 10 m (componentes u y v)

Temperatura a 2 m

Punto de rocío a 2 m

Presión atmosférica a nivel del mar y superficie

Precipitación total mensual

Humedad volumétrica del suelo en varias capas

3.3 Definición del área y periodo
Área geográfica: Murcia (aproximadamente latitud 36.5-39 N, longitud -2.5 a -0.5 E)

Periodo: desde 2015 hasta 2025, datos mensuales

3.4 Descarga de datos
Se generan tres peticiones separadas a la API cdsapi para descargar:

Variables atmosféricas

Precipitación total

Humedad del suelo

Cada petición se configura con los parámetros apropiados (product_type, variable, year, month, time, area) y se descarga el archivo en formato NetCDF.

4. Procesamiento y unión de datos
4.1 Lectura de archivos NetCDF
Se utiliza xarray para abrir cada uno de los archivos NetCDF descargados:

import xarray as xr
atmosfericas = xr.open_dataset("atmosfericas.nc")
precipitacion = xr.open_dataset("precipitacion.nc")
humedad_suelo = xr.open_dataset("humedad_suelo.nc")

4.2 Unión de datasets
Dado que los archivos contienen variables distintas con coordenadas comunes (time, lat, lon), se unen en un solo dataset con:

ds_completo = xr.merge([atmosfericas, precipitacion, humedad_suelo], compat="override")
Esto permite trabajar con todas las variables de forma conjunta en un único objeto multidimensional.

5. Visualización de datos
5.1 En Jupyter Notebook
Visualizaciones básicas con Matplotlib o Seaborn para series temporales y mapas.

Exploración interactiva con widgets (por ejemplo, ipywidgets) para seleccionar variables y periodos.

Análisis estadísticos y generación de gráficos para comprender tendencias y patrones.

5.2 Aplicación interactiva con Streamlit
Crear una app en Python que cargue el dataset unido y ofrezca:

Selector de variable climática para mostrar

Selector de año y mes para filtrar datos

Gráficos dinámicos (series temporales, mapas de calor) con Matplotlib o Plotly integrados

Visualización fácil y rápida desde el navegador web

Ejecutar con:

streamlit run app.py
Streamlit permite desplegar resultados de forma sencilla, ideal para compartir con usuarios no técnicos.

6. Resumen
El flujo completo para trabajar con datos Copernicus incluye:

Registro y configuración de API

Definición de variables, área y periodo

Descarga segmentada de datos en formato NetCDF

Procesamiento y fusión con xarray para análisis conjunto

Visualización exploratoria en Jupyter y creación de apps interactivas con Streamlit

Este proceso permite realizar análisis climáticos avanzados con tecnologías modernas y accesibles para científicos de datos e investigadores.

-----------------------------------------------------------------------------------------------------------------------------
Notebook básico para análisis y visualización en Jupyter

# Importar librerías
import xarray as xr
import matplotlib.pyplot as plt
import streamlit as st  # Solo para referencia en la app, no en Jupyter

# Cargar dataset unido
ds = xr.open_dataset("datos_unidos.nc")

# Mostrar resumen del dataset
print(ds)

# Seleccionar variable para graficar, por ejemplo temperatura a 2m
var = "t2m"

# Extraer serie temporal promedio para toda el área
ts = ds[var].mean(dim=["latitude", "longitude"])

# Graficar serie temporal mensual
plt.figure(figsize=(12,6))
ts.plot()
plt.title(f"Serie temporal mensual de {var}")
plt.ylabel("Valor")
plt.show()

----------------------------------------------------------------------------------------------------------------------------
App Streamlit mínima para visualización interactiva
Guarda esto en app.py:

import streamlit as st
import xarray as xr
import matplotlib.pyplot as plt

# Cargar dataset
ds = xr.open_dataset("datos_unidos.nc")

st.title("Visualización Datos Climáticos Copernicus")

# Variables disponibles en el dataset
variables = list(ds.data_vars)

# Selector variable
var = st.selectbox("Selecciona variable climática:", variables)

# Selector año y mes
años = ds.time.dt.year.values
años_unicos = sorted(set(años))
año_sel = st.selectbox("Selecciona año:", años_unicos)

meses = ds.time.dt.month.values
meses_unicos = sorted(set(meses))
mes_sel = st.selectbox("Selecciona mes:", meses_unicos)

# Filtrar dataset por año y mes
ds_filtrado = ds.sel(time=str(año_sel) + "-" + f"{mes_sel:02d}")

# Extraer datos para la variable seleccionada
data = ds_filtrado[var]

# Graficar con matplotlib
fig, ax = plt.subplots(figsize=(8,6))
data.plot(ax=ax)
ax.set_title(f"{var} en {año_sel}-{mes_sel:02d}")

st.pyplot(fig)

Ejecuta con:
streamlit run app.py