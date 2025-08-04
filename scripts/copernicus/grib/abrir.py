import xarray as xr

archivo = "datos_mensuales_2015_2025.grib"
ds = xr.open_dataset(archivo, engine="cfgrib")

print(ds)
