import json
import pandas as pd
import os
import unicodedata

# Rutas
carpeta_entrada = 'src/data/originales/AEMET/alcantarilla/diarios/'
carpeta_salida = 'src/data/limpios/'
archivo_final = os.path.join(carpeta_salida, 'diarios.csv')

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

def limpiar_archivo(ruta_archivo):
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

        return df

    except Exception as e:
        print(f"❌ Error procesando {ruta_archivo}: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío si falla

def main():
    archivos = [f for f in os.listdir(carpeta_entrada) if f.endswith('.txt')]
    dataframes = []

    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_entrada, archivo)
        df = limpiar_archivo(ruta_archivo)

        if not df.empty:
            dataframes.append(df)

    if dataframes:
        df_final = pd.concat(dataframes, ignore_index=True)
        df_final = df_final.sort_values(by='fecha')
        df_final.to_csv(archivo_final, index=False, encoding='utf-8-sig')
        print(f"\n✅ Todos los datos diarios limpios se han unido en: {archivo_final}")
    else:
        print("⚠️ No se generó el archivo final porque no hay datos limpios.")

if __name__ == "__main__":
    main()
