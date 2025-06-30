import json
import pandas as pd
import os
import unicodedata

# Rutas
carpeta_entrada = 'src/data/originales/AEMET/alcantarilla/mensual-anual/'
carpeta_salida = 'src/data/limpios/'

# Crear carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# Columnas numéricas a limpiar
columnas_numericas = [
    'tmed', 'prec', 'tmin', 'tmax',
    'velmedia', 'racha', 'presMax', 'presMin',
    'hrMedia', 'hrMax', 'hrMin', 'sol'
]

def normalizar_texto(texto):
    if not isinstance(texto, str):
        return texto
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('ASCII')
    return texto

def limpiar_archivo(ruta_archivo, ruta_salida):
    try:
        with open(ruta_archivo, 'r', encoding='latin1') as f:
            datos = json.load(f)

        df = pd.DataFrame(datos)

        # Limpiar columnas numéricas
        for col in columnas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].str.replace(',', '.', regex=False), errors='coerce')

        # Convertir fecha
        if 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], format='%Y-%m-%d')

        # Normalizar texto en 'nombre'
        if 'nombre' in df.columns:
            df['nombre'] = df['nombre'].apply(normalizar_texto)

        df.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
        print(f"✅ Archivo limpio guardado: {ruta_salida}")

    except Exception as e:
        print(f"❌ Error procesando {ruta_archivo}: {e}")

def main():
    archivos = [f for f in os.listdir(carpeta_entrada) if f.endswith('.txt')]

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_entrada, archivo)
        nombre_salida = archivo.replace(' ', '_').replace('.txt', '.csv')
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)

        limpiar_archivo(ruta_archivo, ruta_salida)

if __name__ == "__main__":
    main()
