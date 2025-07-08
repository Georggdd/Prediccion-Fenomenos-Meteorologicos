import json
import pandas as pd
import os
import unicodedata

# === Rutas relativas al script ===
base_dir = os.path.dirname(os.path.abspath(__file__))

carpeta_entrada = os.path.join(base_dir, '../src/data/originales/datos_anuales/')
carpeta_salida = os.path.join(base_dir, '../src/data/limpios/anuales/')

# Crear carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# Columnas que realmente queremos conservar
columnas_utiles = [
    'fecha', 'nombre_estacion',
    'tm_min', 'tm_max', 'tm_mes',
    'ta_min', 'ta_max',
    'p_mes', 'p_max',
    'q_min', 'q_max', 'q_med', 'q_mar',
    'hr', 'inso', 'p_sol',
    'w_med', 'w_racha', 'w_rec'
]

# Columnas numéricas puras
columnas_numericas = [
    'tm_min', 'tm_max', 'tm_mes',
    'ta_min', 'ta_max',
    'p_mes',
    'q_min', 'q_max', 'q_med', 'q_mar',
    'hr', 'inso', 'p_sol',
    'w_med'
]

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return texto
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('ASCII')
    return texto

def limpiar_valor_numero_principal(valor):
    if isinstance(valor, str):
        return valor.split('(')[0].replace(',', '.')
    return valor

def limpiar_archivo(ruta_archivo, ruta_salida):
    try:
        with open(ruta_archivo, 'r', encoding='latin1') as f:
            datos = json.load(f)

        df = pd.DataFrame(datos)

        # Filtrar solo registros anuales (fecha termina en "-13")
        df = df[df['fecha'].str.endswith('-13')]

        # Filtrar solo columnas útiles
        df = df[[col for col in columnas_utiles if col in df.columns]]

        # Normalizar nombre de la estación
        if 'nombre_estacion' in df.columns:
            df['nombre_estacion'] = df['nombre_estacion'].apply(normalizar_texto)

        # Limpiar columnas numéricas
        for col in columnas_numericas:
            if col in df.columns:
                df[col] = df[col].apply(limpiar_valor_numero_principal)
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Convertir 'fecha' de "AAAA-13" a datetime con "AAAA-01-01"
        if 'fecha' in df.columns:
            df['fecha'] = df['fecha'].str.extract(r'(\d{4})')[0]  # Extrae el año
            df['fecha'] = pd.to_datetime(df['fecha'] + '-01-01')

        # Ordenar por año ascendente
        df = df.sort_values(by='fecha')

        # Guardar CSV limpio
        df.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
        print(f"✅ Archivo limpio guardado: {ruta_salida}")

    except Exception as e:
        print(f"❌ Error procesando {ruta_archivo}: {e}")

def main():
    archivos = [f for f in os.listdir(carpeta_entrada) if f.endswith('.txt') or f.endswith('.json')]

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_entrada, archivo)
        nombre_salida = archivo.replace(' ', '_').replace('.txt', '.csv').replace('.json', '.csv')
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)

        limpiar_archivo(ruta_archivo, ruta_salida)

if __name__ == "__main__":
    main()
