import xarray as xr
import matplotlib.pyplot as plt

# Carga dataset unido
ds = xr.open_dataset("datos_unidos.nc")

# Visualizar algunas variables
# Elegimos el primer mes: 2015-01 (index 0)
time_index = 0

# Variables a visualizar
variables = ["t2m", "tp", "swvl1"]  # temperatura 2m, precipitación total, humedad suelo capa 1
titles = ["Temperatura a 2m (K)", "Precipitación total (m)", "Humedad volumétrica suelo capa 1"]

fig, axs = plt.subplots(1, 3, figsize=(18, 5))

for i, var in enumerate(variables):
    data = ds[var].isel(valid_time=time_index)  # seleccionamos el tiempo
    im = data.plot(ax=axs[i], cmap='viridis', add_colorbar=True)
    axs[i].set_title(titles[i])

plt.suptitle(f"Variables climáticas - {str(ds.valid_time[time_index].values)[:10]}")
plt.tight_layout()
plt.show()
