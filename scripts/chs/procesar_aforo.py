import os
import pandas as pd

# Ruta base (carpeta donde está este script)
base_path = os.path.dirname(os.path.abspath(__file__))

# Archivos de entrada y salida en la misma carpeta
input_path = os.path.join(base_path, 'todos_aforo.csv')
output_path = os.path.join(base_path, 'todos_aforo_limpio.csv')

# Cargar CSV
df = pd.read_csv(input_path, sep=',', decimal=',', dtype=str)

# Convertir columna de fecha a datetime
df['Fecha medida'] = pd.to_datetime(df['Fecha medida'], dayfirst=True)

# Limpiar y convertir la columna de nivel
df['Nivel medio diario (m)'] = (
    df['Nivel medio diario (m)']
    .str.replace(',', '.', regex=False)  # cambia coma decimal por punto
    .astype(float)                       # convierte a float
)

# OJO: Ya no eliminamos las filas con NaN

# Guardar CSV limpio
df.to_csv(output_path, index=False, float_format='%.3f')

print(f"Archivo limpio guardado en: {output_path}")
