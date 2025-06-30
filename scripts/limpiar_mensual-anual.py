import json
import pandas as pd
import os
import re

# Rutas
carpeta_entrada = 'src/data/originales/AEMET/alcantarilla/mensuales-anuales/'
carpeta_salida = 'src/data/limpios/'
os.makedirs(carpeta_salida, exist_ok=True)

# Columnas numéricas a limpiar
columnas_numericas = [
    'p_max', 'n_cub', 'hr', 'n_gra', 'n_fog', 'inso', 'q_max', 'nw_55', 'q_mar', 'q_med',
    'tm_min', 'ta_max', 'ts_min', 'nt_30', 'nv_0050', 'n_des', 'np_100', 'n_nub', 'p_sol',
    'nw_91', 'np_001', 'ta_min', 'e', 'np_300', 'nv_1000', 'evap', 'p_mes', 'n_llu', 'n_tor',
    'nt_00', 'ti_max', 'n_nie', 'tm_mes', 'tm_max', 'nv_0100', 'q_min', 'np_010'
]

def limpiar_valor(valor):
    if not isinstance(valor, str):
        return valor
    valor = re.sub(r'\(.*?\)', '', valor)  # Quitar paréntesis y su contenido
    valor = valor.replace(',', '.')        # Convertir coma en punto
    return valor.strip()

# DataFrames acumulativos
mensuales_df = pd.DataFrame()
anuales_df = pd.DataFrame()

# Procesar archivos
for archivo in os.listdir(carpeta_entrada):
    if archivo.endswith('.txt'):
        ruta = os.path.join(carpeta_entrada, archivo)
        try:
            with open(ruta, 'r', encoding='latin1') as f:
                datos = json.load(f)

            df = pd.DataFrame(datos)

            # Limpiar columnas numéricas
            for col in columnas_numericas:
                if col in df.columns:
                    df[col] = df[col].apply(limpiar_valor)
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Extraer anio y mes
            if 'fecha' in df.columns:
                df['fecha'] = df['fecha'].astype(str)
                df['anio'] = df['fecha'].apply(lambda x: int(x.split('-')[0]) if '-' in x else None)
                df['mes'] = df['fecha'].apply(lambda x: int(x.split('-')[1]) if '-' in x else None)

                # Generar campo fecha solo si el mes es válido (1-12)
                df['fecha'] = df.apply(
                    lambda row: pd.to_datetime(f"{row['anio']}-{row['mes']:02}-01") 
                    if pd.notnull(row['anio']) and pd.notnull(row['mes']) and 1 <= row['mes'] <= 12
                    else pd.NaT,
                    axis=1
                )

                # Separar registros
                mensuales = df[df['mes'] <= 12]
                anuales = df[df['mes'] == 13]

                mensuales_df = pd.concat([mensuales_df, mensuales], ignore_index=True)
                anuales_df = pd.concat([anuales_df, anuales], ignore_index=True)

            print(f"✅ Procesado: {archivo}")

        except Exception as e:
            print(f"❌ Error en {archivo}: {e}")

# Ordenar antes de guardar
mensuales_df = mensuales_df.sort_values(by=['anio', 'mes'])
anuales_df = anuales_df.sort_values(by='anio')

# Guardar resultados
mensuales_df.to_csv(os.path.join(carpeta_salida, 'mensuales.csv'), index=False, encoding='utf-8-sig')
anuales_df.to_csv(os.path.join(carpeta_salida, 'anuales.csv'), index=False, encoding='utf-8-sig')

print("\n✅ Archivos guardados correctamente: mensuales.csv y anuales.csv")
