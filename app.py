# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, r2_score

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(layout="wide")
st.title("🌦️ Visualización de modelos climáticos - Alcantarilla (Murcia)")

# Cargar datos
@st.cache_data
def cargar_datos():
    diarios = pd.read_csv('src/data/limpios/AEMET/alcantarilla/diarios/diarios.csv')
    mensuales = pd.read_csv('src/data/limpios/AEMET/alcantarilla/mensuales-anuales/mensuales.csv')
    anuales = pd.read_csv('src/data/limpios/AEMET/alcantarilla/mensuales-anuales/anuales.csv')
    return diarios, mensuales, anuales

df_diarios, df_mensuales, df_anuales = cargar_datos()

# --------- SECCIÓN 1: Datos diarios ----------
st.header("📅 Visualización de datos diarios")

columna = st.selectbox("Selecciona la variable a visualizar", df_diarios.columns[5:25])
df_diarios['fecha'] = pd.to_datetime(df_diarios['fecha'])

fig1, ax1 = plt.subplots(figsize=(12, 5))
ax1.plot(df_diarios['fecha'], df_diarios[columna])
ax1.set_title(f'{columna} diaria')
ax1.set_xlabel("Fecha")
ax1.set_ylabel(columna)
plt.xticks(rotation=45)
st.pyplot(fig1)

# --------- SECCIÓN 2: Clasificación de lluvia ----------
st.header("🌧️ Clasificación: ¿Llovió o no? (Árbol de Decisión)")

df_diarios['lluvia'] = (df_diarios['prec'] > 0).astype(int)
features = ['tmed', 'tmin', 'tmax', 'velmedia', 'racha', 'presMax', 'presMin', 'hrMedia', 'sol']
X = df_diarios[features].fillna(0)
y = df_diarios['lluvia']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
score_train = clf.score(X_train, y_train)
score_test = clf.score(X_test, y_test)
y_pred_clf = clf.predict(X_test)

st.subheader("Resultados:")
st.markdown(f"🎯 Precisión en entrenamiento: `{score_train:.2f}`")
st.markdown(f"🧪 Precisión en prueba: `{score_test:.2f}`")

# Matriz de confusión
fig2, ax2 = plt.subplots()
cm = confusion_matrix(y_test, y_pred_clf)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(ax=ax2)
st.pyplot(fig2)

# --------- SECCIÓN 3: Regresión de cantidad de lluvia ----------
st.header("🌧️📈 Regresión: Predecir cantidad de lluvia (solo días lluviosos)")

dias_lluvia = df_diarios[df_diarios['prec'] > 0]
X_prec = dias_lluvia[features].fillna(0)
y_prec = dias_lluvia['prec']
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_prec, y_prec, test_size=0.2, random_state=42)

reg = LinearRegression()
reg.fit(X_train_reg, y_train_reg)
y_pred_reg = reg.predict(X_test_reg)

r2_train = reg.score(X_train_reg, y_train_reg)
r2_test = reg.score(X_test_reg, y_test_reg)

st.subheader("Resultados:")
st.markdown(f"🎯 R² entrenamiento: `{r2_train:.2f}`")
st.markdown(f"🧪 R² prueba: `{r2_test:.2f}`")

# Gráfico real vs predicción
fig3, ax3 = plt.subplots()
ax3.scatter(y_test_reg, y_pred_reg, alpha=0.5)
ax3.plot([0, max(y_test_reg)], [0, max(y_test_reg)], 'r--')
ax3.set_xlabel("Cantidad real de lluvia")
ax3.set_ylabel("Cantidad predicha")
ax3.set_title("Predicción vs Real - Regresión")
st.pyplot(fig3)

# --------- SECCIÓN 4: LSTM para temperatura media ----------
st.header("🌡️ Serie temporal: Predecir temperatura media con LSTM")

serie = df_diarios['tmed'].fillna(method='ffill').values
scaler = MinMaxScaler()
serie_scaled = scaler.fit_transform(serie.reshape(-1, 1))

def crear_secuencias(data, pasos=5):
    X_seq, y_seq = [], []
    for i in range(len(data) - pasos):
        X_seq.append(data[i:i+pasos])
        y_seq.append(data[i+pasos])
    return np.array(X_seq), np.array(y_seq)

pasos = 5
X_lstm, y_lstm = crear_secuencias(serie_scaled, pasos)
split = int(len(X_lstm) * 0.8)
X_train_lstm, X_test_lstm = X_lstm[:split], X_lstm[split:]
y_train_lstm, y_test_lstm = y_lstm[:split], y_lstm[split:]

model = Sequential()
model.add(Input(shape=(pasos, 1)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')
early_stop = EarlyStopping(monitor='val_loss', patience=5)

history = model.fit(
    X_train_lstm, y_train_lstm,
    epochs=50,
    batch_size=32,
    validation_data=(X_test_lstm, y_test_lstm),
    callbacks=[early_stop],
    verbose=0
)

# Visualizar curva de error
st.subheader("Evolución del error (LSTM)")
fig4, ax4 = plt.subplots()
ax4.plot(history.history['loss'], label="Entrenamiento")
ax4.plot(history.history['val_loss'], label="Validación")
ax4.set_title("Pérdida (MSE)")
ax4.set_ylabel("Error")
ax4.set_xlabel("Época")
ax4.legend()
st.pyplot(fig4)

# Predicción real vs predicha en temperatura
y_pred_lstm = model.predict(X_test_lstm)
y_test_inv = scaler.inverse_transform(y_test_lstm)
y_pred_inv = scaler.inverse_transform(y_pred_lstm)

fig5, ax5 = plt.subplots(figsize=(12, 4))
ax5.plot(y_test_inv, label="Real")
ax5.plot(y_pred_inv, label="Predicha")
ax5.set_title("Temperatura media - Real vs Predicha (LSTM)")
ax5.legend()
st.pyplot(fig5)
