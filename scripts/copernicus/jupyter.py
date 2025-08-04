import xarray as xr
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider

# Carga el dataset unido
ds = xr.open_dataset("datos_unidos.nc")

variables = ["t2m", "tp", "swvl1"]
titles = ["Temperatura a 2m (K)", "Precipitación total (m)", "Humedad suelo capa 1"]

def plot_mes(mes_idx):
    plt.figure(figsize=(18, 5))
    for i, var in enumerate(variables):
        plt.subplot(1, 3, i+1)
        ds[var].isel(valid_time=mes_idx).plot(cmap='viridis')
        plt.title(titles[i])
    plt.suptitle(f"Mes: {str(ds.valid_time[mes_idx].values)[:10]}")
    plt.tight_layout()
    plt.show()

interact(plot_mes, mes_idx=IntSlider(min=0, max=len(ds.valid_time)-1, step=1, value=0))
