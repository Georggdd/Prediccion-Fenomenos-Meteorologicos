import cdsapi
import zipfile
import xarray as xr
import os
from datetime import date, timedelta
import csv

client = cdsapi.Client()

def extraer_media_variable(grib_file, var_name, conversion=None):
    try:
        # Abrir sin filtro y comprobar si la variable existe
        ds = xr.open_dataset(grib_file, engine='cfgrib')
        if var_name not in ds.variables:
            print(f"Variable {var_name} no encontrada en {grib_file}")
            return None
        valor = ds[var_name].mean(dim=['latitude', 'longitude']).values.item()
        if conversion:
            valor = conversion(valor)
        return valor
    except Exception as e:
        print(f"Error leyendo {var_name}: {e}")
        return None

def descargar_y_valores_diarios(year, month, day):
    zip_target = f'murcia_era5land_{year}_{month:02d}_{day:02d}.zip'
    if not os.path.exists(zip_target):
        print(f"Descargando {zip_target} ...")
        client.retrieve('reanalysis-era5-land', {
            'variable': ['2m_temperature', 'total_precipitation', 'surface_pressure'],
            'year': str(year),
            'month': f'{month:02d}',
            'day': f'{day:02d}',
            'time': ['12:00'],
            'format': 'grib',
            'area': [38, -2.5, 37, -1.5],
        }, zip_target)
        print(f"{zip_target} descargado.")
    else:
        print(f"{zip_target} ya existe, no se descarga.")

    with zipfile.ZipFile(zip_target, 'r') as zip_ref:
        zip_ref.extractall()
        grib_file = next((f for f in zip_ref.namelist() if f.endswith(('.grib', '.grb'))), None)
        if grib_file is None:
            raise FileNotFoundError("No se encontró archivo .grib dentro del ZIP")

    # Extraer variables directamente
    t2m = extraer_media_variable(grib_file, 't2m', lambda v: v - 273.15)
    tp = extraer_media_variable(grib_file, 'tp', lambda v: v * 1000)
    sp = extraer_media_variable(grib_file, 'sp', lambda v: v / 100)

    return {'t2m': t2m, 'tp': tp, 'sp': sp}

def descargar_rango_guardar_csv(fecha_inicio, fecha_fin, archivo_csv):
    datos = []
    delta = (fecha_fin - fecha_inicio).days
    for i in range(delta + 1):
        dia = fecha_inicio + timedelta(days=i)
        print(f"Procesando {dia}...")
        valores = descargar_y_valores_diarios(dia.year, dia.month, dia.day)
        fila = {'fecha': dia.isoformat(), **valores}
        datos.append(fila)

    campos = ['fecha', 't2m', 'tp', 'sp']
    with open(archivo_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos)

    print(f"Archivo {archivo_csv} guardado.")

if __name__ == '__main__':
    from datetime import date

    fecha_inicio = date(2025, 1, 1)
    fecha_fin = date(2025, 1, 31)  # Todo enero 2025
    descargar_rango_guardar_csv(fecha_inicio, fecha_fin, 'datos_murcia_enero_2025.csv')