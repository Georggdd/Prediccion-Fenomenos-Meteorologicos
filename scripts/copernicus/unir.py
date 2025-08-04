import xarray as xr

def cargar_y_unir_datos():
    print("Cargando archivos NetCDF existentes...")
    atmosfericas = xr.open_dataset("atmosfericas.nc")
    precipitacion = xr.open_dataset("precipitacion.nc")
    humedad_suelo = xr.open_dataset("humedad_suelo.nc")

    print("Uniendo datasets...")
    ds_completo = xr.merge([atmosfericas, precipitacion, humedad_suelo], compat="override")

    print("Guardando dataset combinado en 'datos_unidos.nc'...")
    ds_completo.to_netcdf("datos_unidos.nc")

    print("\nResumen del dataset combinado:")
    print(ds_completo)

    return ds_completo

if __name__ == "__main__":
    ds = cargar_y_unir_datos()
