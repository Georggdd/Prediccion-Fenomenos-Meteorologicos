# Predicción de Fenómenos Meteorológicos

📌 Descripción

Este proyecto desarrolla un sistema predictivo para fenómenos meteorológicos extremos en la Región de Murcia, centrado en lluvias intensas y DANA, y sus consecuencias como inundaciones.

Se integran datos históricos de AEMET y CHS (2015–2025) y se aplican modelos de IA y Big Data. Además, incluye una aplicación web interactiva en Streamlit para explorar predicciones y variables climáticas/hidrológicas.

🎯 Objetivos

Clasificar días con lluvia intensa.

Estimar la cantidad de precipitación en días lluviosos.

Predecir la evolución temporal de la temperatura media.

Visualizar resultados de forma interactiva.

Demostrar el uso de IA y Big Data para gestión de riesgos climáticos.

## 🚀 ¿Qué es Streamlit?

[Streamlit](https://streamlit.io/) es una herramienta de Python que permite crear interfaces web de forma rápida y sencilla, sin necesidad de conocimientos en desarrollo web. Ideal para prototipos de visualización de datos, dashboards o aplicaciones de machine learning.

Con una sola línea (`streamlit run app.py`), puedes visualizar datos, resultados y modelos en un navegador.

---

🛠️ Metodología
<details> <summary><b>1. Recolección de datos</b></summary>

AEMET: Datos diarios (2015–2025) de todas las estaciones de Murcia vía API REST. Se transformaron de JSON a CSV y se limpiaron variables clave: temperatura mínima, máxima y media, precipitación y humedad relativa.

CHS: Datos hidrológicos diarios (caudales, niveles de ríos y embalses) descargados en CSV y limpiados para integrarlos con los datos meteorológicos.

</details> <details> <summary><b>2. Preprocesamiento</b></summary>

Unificación de datos en un dataframe consolidado.

Limpieza de valores faltantes (reemplazo por medianas).

Normalización de variables numéricas.

Construcción de variables temporales (día, mes, estación del año) y variable binaria inundación (precipitación ≥ 20 mm).

</details> <details> <summary><b>3. Modelado</b></summary>

Árbol de decisión → Clasificación lluvia/no lluvia (precisión, recall, F1).

Regresión lineal → Estimación de precipitación (MSE).

Red neuronal LSTM → Predicción de temperatura media (RMSE).

Random Forest → Predicción de inundaciones, balanceo con SMOTE, búsqueda de hiperparámetros, importancia de variables.

</details> <details> <summary><b>4. Visualización</b></summary>

Streamlit: Aplicación interactiva para consultar probabilidades de inundación y explorar variables climáticas/hidrológicas.

Flujo de trabajo: carga y preprocesamiento → entrenamiento → predicción → visualización interactiva.

Controles interactivos: umbral de decisión, selección de variables y exploración de escenarios.

---

</details>
📊 Resultados

Integración de datos AEMET + CHS (2015–2025).

Modelos con rendimiento satisfactorio y capacidad para detectar patrones meteorológicos relevantes.

Aplicación Streamlit funcional y fácil de usar.

---

💻 Requisitos

Instala las dependencias con:

pip install -r requirements.txt


Principales librerías:

Procesamiento: numpy, pandas, xarray, netCDF4

Machine Learning: scikit-learn, tensorflow, keras, imbalanced-learn

Visualización: matplotlib, seaborn, altair, streamlit

Descarga de datos: requests, cdsapi

---

🚀 Uso

Clonar repositorio:

git clone <https://github.com/Georggdd/Prediccion-Fenomenos-Meteorologicos>
cd <Prediccion-Fenomenos-Meteorologicos>


Instalar dependencias:

pip install -r requirements.txt


Ejecutar la app:

streamlit run Scripts/streamlit_app.py


Explorar predicciones y variables climáticas/hidrológicas.

---

## 📁 Estructura del proyecto

Nueva carpeta/
│
├── .venv310
├── scripts/
│ └── aemet/
│ └── chs/
│ └── datos/
│ └── graficas_modelo/
│ ├── modelos
│ └── prediccion_rf.py
│ ├── streamlit_app.py
│ └── entrenar_modelo_final.py
├──src/data
│ └── aemet/
│ └── chs/
├──.gitignore
├──README
├──requierements

---

👩 Autor

Florentina Georgiana Dumitru
Trabajo de Fin de Máster en Big Data e Inteligencia Artificial – Predicción de fenómenos meteorológicos extremos en Murcia.

 
