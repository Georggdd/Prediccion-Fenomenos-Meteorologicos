# Entrenamiento de modelos

Explicación de los modelos usados, configuración, validación y métricas.

Ejemplo:
- Árboles de decisión para clasificación.
- Modelos de regresión para predicción de magnitud.
- LSTM para series temporales.
- Dividir datos en entrenamiento y test.
- Uso de TensorFlow/Keras.

# Explicación del 1er notebook en jupyter de prueba:

# Celda 1 - Importar librerías necesarias
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

# Explicación celda
 Librerías de manipulación de datos:
| `pandas` (`pd`) | Sirve para leer, limpiar y manipular datos (como tablas de Excel). Es el alma del análisis de datos en Python. |
| `numpy` (`np`)  | Trabaja con arrays y operaciones matemáticas. Muy útil para cálculos numéricos


Librerías de Machine Learning (aprendizaje automático):
| `train_test_split`       | Sirve para dividir los datos en **entrenamiento y prueba** (algo esencial para entrenar modelos).                                |
| `DecisionTreeClassifier` | Un modelo de clasificación basado en árboles de decisión (lo usaremos para clasificar eventos extremos como sequía o no sequía). |
| `LinearRegression`       | Modelo de regresión (lo usaremos para predecir **valores numéricos**, como temperatura o precipitación).                         |


Librerías de Deep Learning (redes neuronales):
| `Sequential`    | Es una forma simple de construir redes neuronales en **TensorFlow/Keras**.                           |
| `LSTM`          | Tipo de red neuronal diseñada para **series temporales**, como los datos meteorológicos.             |
| `Dense`         | Capa de neuronas tradicional (la más básica).                                                        |
| `EarlyStopping` | Detiene el entrenamiento automáticamente si el modelo ya no mejora (evita que “memorice” los datos). |


Librerías de visualización:
| `matplotlib.pyplot` (`plt`) | Sirve para hacer gráficos y visualizar datos y resultados. |

# Resultados
No imprime nada, solo carga las herramientas. Si no da error, está todo en órden.

-------------------------------------------------------------------------------------------------------------------------------

# Celda 2 - Cargar datos limpios (ajusta las rutas a tus archivos)
df_diarios = pd.read_csv('src/data/limpios/AEMET/alcantarilla/diarios/diarios.csv')
df_mensuales = pd.read_csv('src/data/limpios/AEMET/alcantarilla/mensuales-anuales/mensuales.csv')
df_anuales = pd.read_csv('src/data/limpios/AEMET/alcantarilla/mensuales-anuales/anuales.csv')

print("Datos diarios cargados:", df_diarios.shape)
print("Datos mensuales cargados:", df_mensuales.shape)
print("Datos anuales cargados:", df_anuales.shape)

# Explicación celda
La celda 2 es clave porque carga los datos meteorológicos limpios que se van a usar para entrenar los modelos. 
Lee 3 archivos .csv usando pandas y los convierte en tablas (DataFrames) en Python:
| Variable Python | Contenido                      |
| --------------- | ------------------------------ |
| `df_diarios`    | Datos meteorológicos diarios   |
| `df_mensuales`  | Datos meteorológicos mensuales |
| `df_anuales`    | Datos meteorológicos anuales   |
Además, muestra cuántas filas y columnas tiene cada conjunto de datos.

# Resultados
Y Resultados: Datos diarios cargados: (3830, 25)
Datos mensuales cargados: (132, 44)
Datos anuales cargados: (11, 44)

# Explicación resultados
Dataset	        Filas (ejemplos)	Columnas (variables)	Significado
df_diarios	    3830	            25	                    Tienes 3830 días de datos (por ejemplo, desde 2014 a 2024) y                                                           25 variables como temperatura, precipitación, humedad, etc.
df_mensuales	132             	44	                    132 meses de datos, es decir, 11 años × 12 meses y 44 variables.
df_anuales	    11	                44	                    11 años (probablemente desde 2013 a 2023) y 44 variables.


Si sale este mensaje sin errores, es que los archivos se han cargado correctamente y las rutas están bien.
Ahora ya están los datos cargados en memoria y listos para analizarlos o entrenar modelos.
-------------------------------------------------------------------------------------------------------------------------------

# Celda 3 - Exploración rápida de los datos diarios
print(df_diarios.head())
print(df_diarios.info())

# Explicación celda
Esta celda es la primera en la que observamos directamente el contenido y la estructura del dataset diario.

df_diarios.head()
Muestra las primeras 5 filas del DataFrame df_diarios. Esto te da una idea general del contenido del archivo: qué columnas hay, qué tipo de valores, si parecen correctos, etc.

df_diarios.info()
Muestra un resumen técnico del DataFrame:
Número total de filas (3830)
Lista de columnas
Cuántos valores faltan por columna
Tipo de dato de cada columna (float64, int64, object...)

# Resultados
      fecha  indicativo                    nombre provincia  altitud  tmed  \
0  2015-01-01        7228  ALCANTARILLA, BASE AEREA    MURCIA       75   8.6   
1  2015-01-02        7228  ALCANTARILLA, BASE AEREA    MURCIA       75   8.4   
2  2015-01-03        7228  ALCANTARILLA, BASE AEREA    MURCIA       75   9.9   
3  2015-01-04        7228  ALCANTARILLA, BASE AEREA    MURCIA       75  12.2   
4  2015-01-05        7228  ALCANTARILLA, BASE AEREA    MURCIA       75   9.6   

   prec  tmin horatmin  tmax  ...  sol  presMax  horaPresMax  presMin  \
0   0.0   1.5   Varias  15.8  ...  7.3   1028.6           10   1020.8   
1   0.0  -0.4    07:20  17.2  ...  9.0   1030.9           10   1028.1   
2   0.0  -0.4    05:40  20.2  ...  9.1   1030.5           00   1025.9   
3   0.0   2.6    07:15  21.8  ...  9.0   1026.4           00   1020.9   
4   0.0   1.4    07:00  17.9  ...  9.0   1023.2           09   1018.9   

  horaPresMin  hrMedia  hrMax horaHrMax  hrMin horaHrMin  
0          00       67     90     23:10     45     12:20  
1          05       68     97     06:30     31     14:50  
2          18       63     94     06:00     32     14:00  
3          16       48     84    Varias     19     14:40  
4          24       74     97     23:59     50     13:00  

[5 rows x 25 columns]
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3830 entries, 0 to 3829
Data columns (total 25 columns):
 #   Column       Non-Null Count  Dtype  
---  ------       --------------  -----  
 0   fecha        3830 non-null   object 
 1   indicativo   3830 non-null   int64  
 2   nombre       3830 non-null   object 
 3   provincia    3830 non-null   object 
 4   altitud      3830 non-null   int64  
 5   tmed         3830 non-null   float64
 6   prec         3724 non-null   float64
 7   tmin         3830 non-null   float64
 8   horatmin     3830 non-null   object 
 9   tmax         3830 non-null   float64
 10  horatmax     3830 non-null   object 
 11  dir          3797 non-null   float64
 12  velmedia     3807 non-null   float64
 13  racha        3797 non-null   float64
 14  horaracha    3797 non-null   object 
 15  sol          3801 non-null   float64
 16  presMax      3829 non-null   float64
 17  horaPresMax  3829 non-null   object 
 18  presMin      3829 non-null   float64
 19  horaPresMin  3825 non-null   object 
 20  hrMedia      3830 non-null   int64  
 21  hrMax        3830 non-null   int64  
 22  horaHrMax    3830 non-null   object 
 23  hrMin        3830 non-null   int64  
 24  horaHrMin    3830 non-null   object 
dtypes: float64(10), int64(5), object(10)
memory usage: 748.2+ KB
None

# Explicación resultados
✅ Filas y columnas
Hay 3830 filas → son 3830 días de datos.
Hay 25 columnas, que representan variables meteorológicas por día.

✅ Ejemplos de columnas y sus significados
Columna	Descripción
fecha	Día del dato
tmed	Temperatura media del día
prec	Precipitación en mm
tmin, tmax	Temperaturas mínima y máxima
sol	Horas de sol
presMax, presMin	Presiones máxima y mínima
hrMedia, hrMax, hrMin	Humedad relativa media, máxima y mínima
dir, velmedia, racha	Dirección del viento, velocidad media y racha máxima

Algunas columnas como horatmin, horaPresMin, etc., tienen la hora del día en que ocurrió el valor mínimo o máximo.

⚠️ Valores faltantes (missing values)
En el resumen vemos que algunas columnas no tienen los 3830 valores completos:

Columna	    Valores no nulos	Faltantes
prec	    3724	106
dir	        3797	33
velmedia	3807	23
sol	        3801	29

Estas faltas no son muchas, pero conviene tenerlo en cuenta para más adelante: podremos decidir si rellenarlas, eliminarlas o usar alguna técnica especial.

🧮 Tipos de datos
object → texto, fechas o horas.
float64 → números con decimales (temperatura, presión...).
int64 → enteros (altitud, humedad...).

Más adelante convertiremos fecha al tipo datetime para trabajar con el tiempo.

Ahora que se sabe qué contienen los datos diarios, podemos:
- Analizar cómo se comportan las variables en el tiempo.
- Entrenar modelos para predecir cosas como temperatura, lluvia o humedad.
- Buscar correlaciones entre columnas.

-------------------------------------------------------------------------------------------------------------------------------


# Celda 4 - Preparar datos para un modelo simple:  
# Queremos predecir si llovió o no (variable 'prec' > 0)

# Crear columna 'lluvia' binaria: 1 si lluvia > 0, 0 si no
df_diarios['lluvia'] = (df_diarios['prec'] > 0).astype(int)

# Elegimos características (features) numéricas para entrenar
features = ['tmed', 'tmin', 'tmax', 'velmedia', 'racha', 'presMax', 'presMin', 'hrMedia', 'sol']
X = df_diarios[features].fillna(0)  # Rellenar nulos con 0 para simplificar
y = df_diarios['lluvia']

print("Características seleccionadas:", X.columns)

# Explicación celda
🎯 Objetivo:
Predecir si llovió o no en un día usando algunas variables meteorológicas.

✅ Paso 1: Crear la variable objetivo lluvia
df_diarios['lluvia'] = (df_diarios['prec'] > 0).astype(int)
Esto crea una nueva columna llamada lluvia que tiene:
- 1 si sí llovió (prec > 0)
- 0 si no llovió

🔍 Esto transforma un problema de regresión (predecir cuánto llueve) en uno de clasificación binaria: predecimos sí o no.

✅ Paso 2: Selección de características (features)
features = ['tmed', 'tmin', 'tmax', 'velmedia', 'racha', 'presMax', 'presMin', 'hrMedia', 'sol']

Estas son las variables meteorológicas numéricas que usaremos para predecir la lluvia.

Variable	 Significado
tmed	     Temperatura media
tmin	     Temperatura mínima
tmax	     Temperatura máxima
velmedia     Velocidad media del viento
racha	     Racha máxima del viento
presMax	     Presión atmosférica máxima
presMin	     Presión atmosférica mínima
hrMedia	     Humedad relativa media
sol  	     Horas de sol del día

✅ Paso 3: Preparar X e y
X = df_diarios[features].fillna(0)
y = df_diarios['lluvia']

- X son tus variables predictoras.
Se rellenan los valores NaN (faltantes) con 0 para evitar errores (esto es una solución rápida, aunque no siempre ideal).

- y es la etiqueta: si llovió (1) o no (0).

# Resultados
Características seleccionadas: Index(['tmed', 'tmin', 'tmax', 'velmedia', 'racha', 'presMax', 'presMin',
       'hrMedia', 'sol'],
      dtype='object')

# Explicación resultados
Muestra que todo ha ido bien y que las columnas han sido seleccionadas correctamente.

Ahora los datos están listos para entrenar un modelo de predicción.
El siguiente paso será hacer el split en train/test y entrenar un modelo de clasificación, como un árbol de decisión 🌳.
-------------------------------------------------------------------------------------------------------------------------------

# Celda 5 - Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Tamaño de entrenamiento:", X_train.shape)
print("Tamaño de prueba:", X_test.shape)

# Explicación celda
En esta celda 5 estamos dividiendo los datos para poder entrenar y evaluar el modelo correctamente. Vamos a ver con claridad qué significa cada paso.

🎯 Objetivo de esta celda
Separar el conjunto de datos (X, y) en:

- Conjunto de entrenamiento (train) → Para entrenar el modelo.
- Conjunto de prueba (test) → Para evaluar qué tan bien generaliza el modelo a datos nuevos.

✅ Código línea a línea
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

Explicación:
X = datos de entrada (features seleccionadas).
y = etiqueta que queremos predecir (llovió o no).

test_size=0.2 → Reservamos un 20% de los datos para pruebas.
random_state=42 → Semilla para obtener siempre la misma división (importante para reproducibilidad).

Resultado:
X_train: 80% de los datos (3.064 días).
X_test: 20% de los datos (766 días).

✅ Por qué es importante esta división
Sin esta separación:
- El modelo podría “memorizar” los datos en lugar de aprender patrones generales.
- No tendríamos forma de saber si realmente funciona bien con datos nuevos.

# Resultados
Tamaño de entrenamiento: (3064, 9)
Tamaño de prueba: (766, 9)

# Explicación resultados
Cada conjunto contiene 9 columnas (las variables meteorológicas), y el número de filas corresponde a los días.

En el siguiente paso empezamos con el modelo de árbol de decisión

-------------------------------------------------------------------------------------------------------------------------------

# Celda 6 - Entrenar un Árbol de Decisión para clasificación de lluvia
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

score_train = clf.score(X_train, y_train)
score_test = clf.score(X_test, y_test)

print(f"Precisión en entrenamiento: {score_train:.2f}")
print(f"Precisión en prueba: {score_test:.2f}")

# Explicación
Esta celda 6 marca el inicio del modelado predictivo, y usas un Árbol de Decisión para predecir si va a llover o no.

🎯 Objetivo
Entrenar un modelo de clasificación que prediga la probabilidad de lluvia (1 = llovió, 0 = no llovió) usando las variables meteorológicas.

🧠 ¿Qué es un Árbol de Decisión?
Un árbol de decisión es como un flujo de preguntas que se hace el modelo para decidir si un caso pertenece a una clase u otra. Ejemplo:

¿presión baja?
    └─ Sí → ¿temperatura baja?
        └─ Sí → Probabilidad de lluvia alta

✅ Código explicado paso a paso
clf = DecisionTreeClassifier(random_state=42)

Crea el modelo de árbol de decisión.
random_state=42 asegura resultados reproducibles.
----
clf.fit(X_train, y_train)

El modelo se entrena con el 80% de los datos (X_train, y_train).
---

score_train = clf.score(X_train, y_train)
score_test = clf.score(X_test, y_test)

score() calcula la precisión: proporción de predicciones correctas.
En entrenamiento (score_train) → qué tan bien predice los datos con los que se entrenó.
En prueba (score_test) → qué tan bien predice datos nuevos.

# Resultados
Precisión en entrenamiento: 1.00
Precisión en prueba: 0.84

# Explicación resultados 
1.00 en entrenamiento: el modelo memorizó los datos (¡cuidado! esto puede ser sobreajuste).
0.84 en prueba: acierta el 84% de los días nuevos → buen resultado, pero puede mejorar con más limpieza o modelos más complejos.

*Sí. Cuando un modelo tiene 100% de precisión en entrenamiento pero menos en test, probablemente ha aprendido los datos “de memoria” en vez de generalizar. Aún así, 0.84 en test no está mal para un primer intento.*
-------------------------------------------------------------------------------------------------------------------------------

# Celda 7 - Entrenar un modelo de regresión para predecir la cantidad de lluvia (prec)

# Usamos solo días con lluvia para este modelo
precip_dias = df_diarios[df_diarios['prec'] > 0]
X_prec = precip_dias[features].fillna(0)
y_prec = precip_dias['prec']

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_prec, y_prec, test_size=0.2, random_state=42)

reg = LinearRegression()
reg.fit(X_train_reg, y_train_reg)

score_reg_train = reg.score(X_train_reg, y_train_reg)
score_reg_test = reg.score(X_test_reg, y_test_reg)

print(f"R2 en entrenamiento (precipitación): {score_reg_train:.2f}")
print(f"R2 en prueba (precipitación): {score_reg_test:.2f}")

# Explicación
En esta celda 7 estamos pasando de una clasificación a una regresión: ahora no queremos saber si llueve, sino cuánto llueve.

🎯 Objetivo
Predecir la cantidad exacta de lluvia (prec) solo en los días en que llovió (prec > 0), usando un modelo de regresión lineal.

🧠 ¿Qué es la regresión lineal?
Es un modelo que intenta ajustar una línea (o plano, o hiperplano) que relacione las variables independientes (tmed, presMax, etc.) con una variable dependiente (prec en este caso).

Matemáticamente:
prec ≈ b0 + b1*tmed + b2*tmin + ... + b9*sol

 Código explicado
precip_dias = df_diarios[df_diarios['prec'] > 0]

Filtra el DataFrame para quedarse solo con los días lluviosos.
-----

X_prec = precip_dias[features].fillna(0)
y_prec = precip_dias['prec']

Crea las variables X (características) e y (etiqueta a predecir = cantidad de lluvia).
----

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(...)

Divide los datos lluviosos en entrenamiento y prueba.
----

reg = LinearRegression()
reg.fit(X_train_reg, y_train_reg)

Crea y entrena un modelo de regresión lineal.
----

score_reg_train = reg.score(X_train_reg, y_train_reg)
score_reg_test = reg.score(X_test_reg, y_test_reg)

Calcula el R² (R cuadrado), que indica qué proporción de la variabilidad del prec puede explicarse por las variables independientes.

🧮 ¿Qué nos dice el valor de R²?
R² valor	Significado
1.00	Predicción perfecta (casi imposible en el mundo real)
0.90	Muy buen modelo
0.50	Modelo decente
0.10	Modelo débil
< 0.00	Peor que predecir la media
-----

# Resultados 
R2 en entrenamiento (precipitación): 0.17
R2 en prueba (precipitación): 0.07

# Explicación resultados
0.17 en entrenamiento → el modelo explica solo el 17% de la variabilidad de la lluvia en los datos que ha visto.
0.07 en test → solo el 7% en datos nuevos.

Esto nos dice que:
El modelo no predice bien la cantidad de lluvia.
Las relaciones entre las variables y la lluvia no son lineales.

Posiblemente necesitas:
Modelos no lineales (Random Forest, XGBoost, redes neuronales…)
Más variables (ej. humedad relativa, días anteriores, acumulados…)
Datos más limpios (sin outliers, con normalización...)

-------------------------------------------------------------------------------------------------------------------------------


# Celda 8 - Preparar datos para LSTM (serie temporal)

# Vamos a usar la temperatura media diaria para predecir la siguiente

# Ordenar por fecha
df_diarios = df_diarios.sort_values('fecha')

# Seleccionar la columna para la serie temporal
serie = df_diarios['tmed'].fillna(method='ffill').values  # Rellenar con el último valor válido

# Normalizar (escalar) la serie entre 0 y 1 para que LSTM funcione mejor
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
serie_scaled = scaler.fit_transform(serie.reshape(-1,1))

# Función para crear secuencias (ventanas deslizantes)
def crear_secuencias(data, pasos=5):
    X, y = [], []
    for i in range(len(data) - pasos):
        X.append(data[i:i+pasos])
        y.append(data[i+pasos])
    return np.array(X), np.array(y)

pasos = 5
X_lstm, y_lstm = crear_secuencias(serie_scaled, pasos)

# Dividir en entrenamiento y prueba
split = int(len(X_lstm) * 0.8)
X_train_lstm, X_test_lstm = X_lstm[:split], X_lstm[split:]
y_train_lstm, y_test_lstm = y_lstm[:split], y_lstm[split:]

print("Formas de los datos LSTM:", X_train_lstm.shape, y_train_lstm.shape)

# Explicación

Esta celda está dedicada a preparar los datos para alimentar un modelo LSTM que prediga la temperatura media diaria del día siguiente a partir de las temperaturas de días anteriores.

1. Ordenar por fecha
df_diarios = df_diarios.sort_values('fecha')

Aseguramos que la serie temporal esté ordenada cronológicamente para que la secuencia tenga sentido.

2. Seleccionar la serie temporal a predecir
serie = df_diarios['tmed'].fillna(method='ffill').values

Se escoge la columna tmed (temperatura media diaria).
Para los valores nulos, se rellena con el último valor válido anterior (forward fill). Esto es importante para no dejar huecos que rompan la secuencia.
(Nota: aparece un warning indicando que fillna(method='ffill') está obsoleto, es mejor usar directamente df_diarios['tmed'].ffill().)

3. Normalizar los datos
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
serie_scaled = scaler.fit_transform(serie.reshape(-1,1))

Se escala la serie para que sus valores estén entre 0 y 1. Esto es fundamental para que la red neuronal LSTM aprenda mejor y de forma más estable, porque las activaciones funcionan mejor en rangos reducidos.

4. Crear secuencias con ventanas deslizantes
def crear_secuencias(data, pasos=5):
    X, y = [], []
    for i in range(len(data) - pasos):
        X.append(data[i:i+pasos])
        y.append(data[i+pasos])
    return np.array(X), np.array(y)
pasos = 5
X_lstm, y_lstm = crear_secuencias(serie_scaled, pasos)

Aquí se crea la estructura de datos para el LSTM:

- asos=5 indica que usaremos las temperaturas de 5 días consecutivos para predecir la temperatura del día siguiente.
- X_lstm será un array de secuencias de 5 días (ventanas de entrada).
- y_lstm será el valor objetivo (temperatura del día siguiente).

Por ejemplo, para la posición i, X[i] son las temperaturas desde el día i hasta i+4, y y[i] es la temperatura del día i+5.

5. Dividir los datos en entrenamiento y prueba
split = int(len(X_lstm) * 0.8)
X_train_lstm, X_test_lstm = X_lstm[:split], X_lstm[split:]
y_train_lstm, y_test_lstm = y_lstm[:split], y_lstm[split:]

Se utiliza un 80% de los datos para entrenar y el 20% restante para evaluar el modelo.
Se respetan las secuencias temporales, no se mezclan datos para evitar "mirar al futuro".

6. Imprimir las formas (shapes) de los datos
print("Formas de los datos LSTM:", X_train_lstm.shape, y_train_lstm.shape)

# Resultados
Formas de los datos LSTM: (3060, 5, 1) (3060, 1)

C:\Users\georg\AppData\Local\Temp\ipykernel_8780\3971590742.py:9: FutureWarning: Series.fillna with 'method' is deprecated and will raise in a future version. Use obj.ffill() or obj.bfill() instead.
  serie = df_diarios['tmed'].fillna(method='ffill').values  # Rellenar con el último valor válido

# Explicación resultados
Esto significa que:

Hay 3060 muestras para entrenamiento.
Cada muestra de entrada X_train_lstm tiene 5 pasos temporales (días), y 1 característica (temperatura).
Cada etiqueta y_train_lstm es un valor único (temperatura siguiente).

(Nota: aparece un warning indicando que fillna(method='ffill') está obsoleto, es mejor usar directamente df_diarios['tmed'].ffill().) El warning sobre fillna es menor y puede corregirse para futuras versiones.

-------------------------------------------------------------------------------------------------------------------------------


# Celda 9 - Crear y entrenar modelo LSTM

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping

model = Sequential()
model.add(Input(shape=(pasos, 1)))   # Capa de entrada explícita para evitar warning
model.add(LSTM(50))                  # Activación por defecto 'tanh'
model.add(Dense(1))

model.compile(optimizer='adam', loss='mse')

early_stop = EarlyStopping(monitor='val_loss', patience=5)

history = model.fit(
    X_train_lstm, y_train_lstm,
    epochs=50,
    batch_size=32,
    validation_data=(X_test_lstm, y_test_lstm),
    callbacks=[early_stop],
    verbose=1
)

# Explicación
Las 3 primeras líneas se importan y permiten construir un modelo secuencial con capas LSTM y Dense, y usar EarlyStopping para evitar sobreentrenar.

*Modelo LSTM*

model.add(Input(shape=(pasos, 1)))   # Capa de entrada explícita para evitar warning

Añades explícitamente la capa de entrada, con una forma (pasos, 1):
- pasos: número de pasos de tiempo (timesteps) que usa el LSTM.
- 1: número de características por paso (feature size).
Esto previene un warning de TensorFlow que aparece si no se especifica la forma de entrada.
---

model.add(LSTM(50))  # Activación por defecto 'tanh'

Añades una capa LSTM con 50 unidades (neuronas).
Esta capa procesa la secuencia de datos de entrada y extrae patrones temporales.
La función de activación predeterminada para la celda LSTM es tanh.
---

model.add(Dense(1))

Añades una capa densa final con 1 neurona, que hace la regresión (salida continua) y entrega la predicción para cada secuencia de entrada.
---

model.compile(optimizer='adam', loss='mse')

Compilas el modelo usando el optimizador Adam, que es un método eficiente para actualizar pesos.
La función de pérdida es MSE (Mean Squared Error), que es adecuada para problemas de regresión.
---

early_stop = EarlyStopping(monitor='val_loss', patience=5)

Defines una callback para parar el entrenamiento si la métrica monitorizada (val_loss) no mejora durante 5 épocas consecutivas (patience=5).
Esto ayuda a evitar sobreentrenamiento y ahorra tiempo computacional.
---

history = model.fit(
    X_train_lstm, y_train_lstm,
    epochs=50,
    batch_size=32,
    validation_data=(X_test_lstm, y_test_lstm),
    callbacks=[early_stop],
    verbose=1
)

Empiezas el entrenamiento del modelo con los datos de entrenamiento (X_train_lstm, y_train_lstm).
Ejecuta hasta 50 épocas, con mini-batches de tamaño 32.
Usa los datos de validación (X_test_lstm, y_test_lstm) para medir el rendimiento después de cada época.
Aplica la parada temprana con la callback early_stop.
verbose=1 muestra el progreso de cada época en la consola.
---

Esta celda crea un modelo LSTM simple para un problema de predicción secuencial/regresión, con una capa LSTM y una capa densa final, entrena con parada temprana basada en la pérdida de validación y muestra el progreso.

# Resultados
Epoch 1/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 2s 6ms/step - loss: 0.0967 - val_loss: 0.0051
Epoch 2/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0052 - val_loss: 0.0041
Epoch 3/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0047 - val_loss: 0.0040
Epoch 4/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0045 - val_loss: 0.0043
Epoch 5/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0048 - val_loss: 0.0040
Epoch 6/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0045 - val_loss: 0.0039
Epoch 7/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0043 - val_loss: 0.0038
Epoch 8/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0043 - val_loss: 0.0037
Epoch 9/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0041 - val_loss: 0.0036
Epoch 10/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0042 - val_loss: 0.0035
Epoch 11/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0040 - val_loss: 0.0035
Epoch 12/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0040 - val_loss: 0.0034
Epoch 13/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0036 - val_loss: 0.0035
Epoch 14/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0037 - val_loss: 0.0033
Epoch 15/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0035 - val_loss: 0.0032
Epoch 16/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0038 - val_loss: 0.0031
Epoch 17/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0036 - val_loss: 0.0031
Epoch 18/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0034 - val_loss: 0.0030
Epoch 19/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0035 - val_loss: 0.0030
Epoch 20/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0033 - val_loss: 0.0030
Epoch 21/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0032 - val_loss: 0.0030
Epoch 22/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0033 - val_loss: 0.0029
Epoch 23/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0033 - val_loss: 0.0028
Epoch 24/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0031 - val_loss: 0.0030
Epoch 25/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0030 - val_loss: 0.0028
Epoch 26/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0030 - val_loss: 0.0030
Epoch 27/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0029 - val_loss: 0.0027
Epoch 28/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0031 - val_loss: 0.0027
Epoch 29/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0031 - val_loss: 0.0026
Epoch 30/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0029 - val_loss: 0.0027
Epoch 31/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0028 - val_loss: 0.0026
Epoch 32/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0030 - val_loss: 0.0026
Epoch 33/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0028 - val_loss: 0.0026
Epoch 34/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0030 - val_loss: 0.0026
Epoch 35/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0027 - val_loss: 0.0026
Epoch 36/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0029 - val_loss: 0.0027
Epoch 37/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0029 - val_loss: 0.0027
Epoch 38/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0029 - val_loss: 0.0026
Epoch 39/50
96/96 ━━━━━━━━━━━━━━━━━━━━ 0s 4ms/step - loss: 0.0030 - val_loss: 0.0029

# Explicación resultados
*Evolución de la pérdida (loss) y la pérdida de validación (val_loss):*

- La pérdida inicial en la primera época es relativamente alta (loss ≈ 0.0967), pero baja rápidamente a partir de la segunda época (loss ≈ 0.0052), lo que indica que el modelo está aprendiendo rápido desde el principio.
- La pérdida de validación también empieza en un valor bajo (~0.0051) y sigue bajando progresivamente hasta valores alrededor de 0.0026 - 0.0030, lo que sugiere que el modelo está generalizando bien a datos que no ha visto durante el entrenamiento.

*Estabilidad y ausencia de sobreajuste:*

- La diferencia entre la pérdida de entrenamiento y la de validación es muy pequeña y se mantiene constante, lo cual es una señal positiva de que no hay un sobreajuste significativo.
- No se observa un aumento en la pérdida de validación con las épocas, que normalmente indicaría que el modelo comienza a memorizar y pierde capacidad de generalización.

*Calidad del ajuste:*

- Los valores de pérdida en torno a 0.0026 para un problema de regresión son generalmente buenos, especialmente si los datos están normalizados. Esto indica que el modelo está haciendo predicciones bastante precisas.
- La evolución muestra una ligera oscilación, pero la tendencia general es a mejorar o mantenerse estable, lo cual es típico cuando el modelo alcanza un buen punto en el espacio de parámetros.
-------------------------------------------------------------------------------------------------------------------------------

# Celda 10 - Visualizar la evolución del error en entrenamiento y prueba

import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='Error entrenamiento')
plt.plot(history.history['val_loss'], label='Error validación')
plt.legend()
plt.show()

# Explicación celda

Esta celda genera un gráfico que muestra cómo evolucionó el error del modelo durante el entrenamiento y la validación a lo largo de las épocas.

plt.plot(history.history['loss'], label='Error entrenamiento')
plt.plot(history.history['val_loss'], label='Error validación')
plt.legend()
plt.show()


history.history['loss']: es la lista del error de entrenamiento (MSE) para cada época.
history.history['val_loss']: es la lista del error de validación para cada época.
Se plotean ambas curvas y se añade una leyenda para identificar cada línea.
Finalmente, se muestra la gráfica.

# Resultados
Gráfica (image.png dentro de la carpeta documentación)

# Explicación resultados
- El error de entrenamiento comienza relativamente alto (~0.06), pero cae muy rápido en las primeras épocas hasta estabilizarse cerca de 0.0025-0.003.
- El error de validación también comienza bajo y se mantiene estable muy cerca del error de entrenamiento.
- Ambas curvas convergen, lo que indica que el modelo no está ni sobreajustando ni subajustando demasiado: tiene un buen ajuste.
- La baja diferencia entre ambos errores muestra que el modelo generaliza bien a datos nuevos.
- La forma plana después de pocas épocas indica que el entrenamiento se estabilizó rápido y probablemente la parada temprana detuvo el entrenamiento cuando ya no mejoraba la validación.
