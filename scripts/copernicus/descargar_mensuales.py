import cdsapi
import xarray as xr

def descargar_datos():
    client = cdsapi.Client()

    years = [str(y) for y in range(2015, 2026)]
    months = [f"{m:02d}" for m in range(1, 13)]
    area = [39, -2.5, 36.5, -0.5]

    # Request 1: variables atmosféricas
    request1 = {
        "product_type": "monthly_averaged_reanalysis",
        "variable": [
            "10m_u_component_of_wind",
            "10m_v_component_of_wind",
            "2m_dewpoint_temperature",
            "2m_temperature",
            "mean_sea_level_pressure",
            "surface_pressure"
        ],
        "year": years,
        "month": months,
        "time": ["00:00"],
        "format": "netcdf",
        "area": area
    }
    print("Descargando variables atmosféricas...")
    client.retrieve("reanalysis-era5-single-levels-monthly-means", request1).download("atmosfericas.nc")

    # Request 2: precipitación total
    request2 = {
        "product_type": "monthly_averaged_reanalysis",
        "variable": ["total_precipitation"],
        "year": years,
        "month": months,
        "time": ["00:00"],
        "format": "netcdf",
        "area": area
    }
    print("Descargando precipitación total...")
    client.retrieve("reanalysis-era5-single-levels-monthly-means", request2).download("precipitacion.nc")

    # Request 3: humedad volumétrica suelo (4 capas)
    request3 = {
        "product_type": "monthly_averaged_reanalysis",
        "variable": [
            "volumetric_soil_water_layer_1",
            "volumetric_soil_water_layer_2",
            "volumetric_soil_water_layer_3",
            "volumetric_soil_water_layer_4"
        ],
        "year": years,
        "month": months,
        "time": ["00:00"],
        "format": "netcdf",
        "area": area
    }
    print("Descargando humedad volumétrica del suelo...")
    client.retrieve("reanalysis-era5-single-levels-monthly-means", request3).download("humedad_suelo.nc")

def cargar_y_unir_datos():
    print("Cargando archivos NetCDF...")
    atmosfericas = xr.open_dataset("atmosfericas.nc")
    precipitacion = xr.open_dataset("precipitacion.nc")
    humedad_suelo = xr.open_dataset("humedad_suelo.nc")

    print("Uniendo datasets...")
    # Unir datasets por coordenadas comunes (time, lat, lon)
    # Si da conflicto con variables o coordenadas, usar merge con compatibilidad 'override'
    ds_completo = xr.merge([atmosfericas, precipitacion, humedad_suelo], compat="override")

    print(ds_completo)
    return ds_completo

if __name__ == "__main__":
    descargar_datos()
    ds = cargar_y_unir_datos()
