# Curva de error (fig4)

Qué es: Un gráfico de líneas con dos curvas:

Entrenamiento: Error (pérdida) que el modelo tiene en los datos con los que aprende.
Validación: Error que el modelo tiene en datos que no ha visto mientras entrena, para medir qué tan bien generaliza.

Qué representa:

El eje X es el número de épocas (iteraciones completas sobre los datos de entrenamiento).
El eje Y es el error, medido aquí como MSE (Mean Squared Error, error cuadrático medio).

Cómo interpretarlo:

Ambas curvas deberían bajar y estabilizarse, indicando que el modelo aprende.
Si la curva de entrenamiento sigue bajando y la de validación sube, puede que haya overfitting (sobreajuste).
En tu gráfico, si ambas bajan y se acercan, indica un buen entrenamiento.

# Gráfico de predicción real vs predicha (fig5)

Qué es: Una gráfica donde se comparan dos series temporales (líneas sobre el mismo eje temporal):

La temperatura real observada en los datos de prueba (línea “Real”).
La temperatura que predijo tu modelo LSTM para esos mismos días (línea “Predicha”).

Qué representa:

El eje X es la secuencia temporal (días o índices).
El eje Y es la temperatura media (en grados, desescalada para estar en su rango original).

Cómo interpretarlo:

Si las líneas están muy próximas y siguen la misma tendencia, el modelo está haciendo buenas predicciones.
Si hay grandes desviaciones o patrones diferentes, el modelo no está capturando bien la dinámica.

¿Por qué usas LSTM aquí?
Porque la temperatura media es una serie temporal, donde el valor de un día depende de los días anteriores. LSTM es una arquitectura diseñada para capturar relaciones a largo plazo en secuencias.

Resumen final:
El primer gráfico te muestra cómo el modelo fue mejorando durante el entrenamiento.
El segundo gráfico te muestra qué tan bien tu modelo predice la temperatura futura a partir de las temperaturas pasadas.