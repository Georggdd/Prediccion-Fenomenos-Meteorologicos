import pandas as pd
import os

# Ruta al archivo limpio
base_dir = os.path.dirname(__file__)
input_path = os.path.join(base_dir, 'todos_aforo_limpio.csv')
output_path = os.path.join(base_dir, 'todos_aforo_ancho.csv')

# Leer el archivo limpio
df = pd.read_csv(input_path, parse_dates=['Fecha medida'])

# Pivotear el DataFrame: fechas como índice, códigos como columnas
df_pivot = df.pivot(index='Fecha medida', columns='Código', values='Nivel medio diario (m)')

# Ordenar por fecha
df_pivot = df_pivot.sort_index()

# Guardar a CSV, manteniendo NaN si faltan valores
df_pivot.to_csv(output_path, float_format='%.3f')

print("✅ Archivo en formato ancho guardado como:", output_path)
