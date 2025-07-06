# Predicción de Fenómenos Meteorológicos

Este proyecto tiene como objetivo predecir fenómenos meteorológicos extremos utilizando técnicas de Machine Learning e Inteligencia Artificial.

# 🌦️ Visualización de Modelos Climáticos con Streamlit

Este proyecto tiene como objetivo analizar y predecir fenómenos meteorológicos en la estación de **Alcantarilla (Murcia)** utilizando técnicas de Machine Learning y Deep Learning, y mostrar los resultados de forma interactiva mediante una app construida con **Streamlit**.

---

## 🚀 ¿Qué es Streamlit?

[Streamlit](https://streamlit.io/) es una herramienta de Python que permite crear interfaces web de forma rápida y sencilla, sin necesidad de conocimientos en desarrollo web. Ideal para prototipos de visualización de datos, dashboards o aplicaciones de machine learning.

Con una sola línea (`streamlit run app.py`), puedes visualizar datos, resultados y modelos en un navegador.

---

## 🧠 Fases del proyecto

### 1. 🔍 Obtención y limpieza de los datos

- Se han descargado datos climáticos diarios, mensuales y anuales de la AEMET.
- Se han unificado, filtrado y limpiado los datos de la estación meteorológica de Alcantarilla.
- Los datos se guardan en formato `.csv` dentro de la carpeta `/src/data/limpios/`.

Tamaños de los datasets:
- **Diarios**: 3830 registros, 25 variables.
- **Mensuales**: 132 registros, 44 variables.
- **Anuales**: 11 registros, 44 variables.

---

### 2. 🧪 Entrenamiento de modelos

#### 🌧️ Clasificación: ¿Llovió o no?
- Variable objetivo: `prec > 0 → lluvia = 1`, `prec = 0 → lluvia = 0`
- Modelo: Árbol de Decisión (`DecisionTreeClassifier`)
- Precisión:
  - Entrenamiento: **100%**
  - Prueba: **84%**

#### 🌧️📈 Regresión: Cantidad de lluvia (solo días lluviosos)
- Variable objetivo: `prec` (precipitación en mm)
- Modelo: Regresión Lineal
- R²:
  - Entrenamiento: **0.17**
  - Prueba: **0.07**

#### 🌡️ Serie temporal: Predicción de temperatura media diaria
- Variable objetivo: `tmed` del día siguiente
- Modelo: Red LSTM con ventana deslizante de 5 días
- Preprocesamiento:
  - Escalado entre 0 y 1
  - Conversión a secuencias (`X`, `y`)
- Métrica: **Error cuadrático medio (`MSE`)**
- Observación: buen ajuste sin sobreajuste, validación estable

---

### 3. 📊 Visualización interactiva con Streamlit

La app `app.py` permite visualizar de forma dinámica:

#### 🗂️ Datos diarios
- Gráficos de evolución temporal de cualquier variable (ej: temperatura, presión, humedad...).

#### 🤖 Clasificación (Árbol de decisión)
- Precisión en entrenamiento y prueba
- Matriz de confusión visual

#### 🔬 Regresión (precipitación)
- Comparación entre valores reales y predichos
- R² en entrenamiento y test
- Gráfico de dispersión

#### 📈 Serie temporal (LSTM)
- Gráfica de pérdida entrenamiento/validación
- Comparación: temperatura real vs predicha

---

## 📁 Estructura del proyecto

proyecto-clima/
│
├── app.py # Aplicación Streamlit
├── README.md # Este archivo
├── src/
│ └── data/
│ └── limpios/
│ └── AEMET/
│ └── alcantarilla/
│ ├── diarios/diarios.csv
│ └── mensuales-anuales/
│ ├── mensuales.csv
│ └── anuales.csv

## 🔧 Requisitos

Primero activa tu entorno virtual:

  .\venv\Scripts\activate

Luego instala las dependencias:

pip install streamlit matplotlib pandas scikit-learn tensorflow

▶️ ¿Cómo ejecutar la app?
Una vez dentro del entorno virtual y con los paquetes instalados:

streamlit run app.py

Se abrirá automáticamente la app en tu navegador.

✨ Autora del proyecto
Este trabajo ha sido realizado por Georgiana como parte de su Trabajo de Fin de Máster en Big Data e Inteligencia Artificial, centrado en la predicción de fenómenos meteorológicos extremos mediante técnicas de IA.