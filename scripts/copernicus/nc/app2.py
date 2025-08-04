import streamlit as st
import xarray as xr
import matplotlib.pyplot as plt

# Carga el dataset unido
ds = xr.open_dataset("datos_unidos.nc")

variables = {
    "Temperatura a 2m (K)": "t2m",
    "Precipitación total (m)": "tp",
    "Humedad suelo capa 1": "swvl1"
}

st.title("Visualización mensual variables climáticas (2015-2025)")

mes_idx = st.slider("Selecciona mes", 0, len(ds.valid_time) - 1, 0)
fecha = str(ds.valid_time[mes_idx].values)[:10]

fig, axs = plt.subplots(1, 3, figsize=(18, 5))

for i, (title, var) in enumerate(variables.items()):
    ds[var].isel(valid_time=mes_idx).plot(ax=axs[i], cmap="viridis", add_colorbar=True)
    axs[i].set_title(title)

st.write(f"Variables climáticas para: {fecha}")
st.pyplot(fig)
