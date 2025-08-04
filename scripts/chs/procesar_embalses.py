import pandas as pd
import unicodedata
import seaborn as sns
import matplotlib.pyplot as plt

# Ruta del archivo CSV (ajusta según tu estructura)
ruta_csv = "todos_embalses.csv"
ruta_salida = "embalses_limpio.csv"

# Función para normalizar nombres de columnas (quitar tildes, diéresis y caracteres especiales)
def normalizar_col(col):
    col = col.strip().lower()
    col = ''.join(c for c in unicodedata.normalize('NFD', col) if unicodedata.category(c) != 'Mn')
    col = col.replace(" ", "_").replace(".", "").replace("(", "").replace(")", "").replace("³", "3")
    return col

# Leer CSV
df = pd.read_csv(ruta_csv, sep=",", encoding="utf-8")

# Normalizar nombres columnas
df.columns = [normalizar_col(col) for col in df.columns]

# Convertir columna de fecha a datetime
df['fec_medida'] = pd.to_datetime(df['fec_medida'], dayfirst=True)

# Columnas numéricas a limpiar y convertir a float
cols_numericas = [
    'evapor_diaria_m3', 
    'desague_diario_m3', 
    'altura_diaria_m', 
    'superf_diaria_m2', 
    'aport_diaria_m3', 
    'volumen_diario_m3'
]

# Limpiar y convertir columnas numéricas
for col in cols_numericas:
    df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

# Guardar datos limpios
df.to_csv(ruta_salida, index=False)
print(f"✅ Datos limpios guardados en: {ruta_salida}")

# Gráfico línea volumen diario por embalse
sns.lineplot(data=df, x="fec_medida", y="volumen_diario_m3", hue="codigo")
plt.title("Volumen diario en embalses")
plt.xlabel("Fecha")
plt.ylabel("Volumen diario (m³)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
