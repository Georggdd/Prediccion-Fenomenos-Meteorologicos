Contexto general

Este bloque hace una regresión lineal para predecir la cantidad de lluvia (en milímetros) solo en los días en los que efectivamente llovió. Es decir, mientras el árbol de decisión anterior clasificaba si llovió o no (variable categórica), aquí intentamos predecir cuánto llovió (variable continua).

Paso a paso del código

1. Filtrar sólo días lluviosos:

dias_lluvia = df_diarios[df_diarios['prec'] > 0]
Se crea un subconjunto del DataFrame con los días en los que la precipitación (prec) fue mayor que cero, descartando los días sin lluvia.

2. Definir variables independientes (X) y dependiente (y):

X_prec = dias_lluvia[features].fillna(0)
y_prec = dias_lluvia['prec']
X_prec: todas las características climáticas seleccionadas (temperaturas, viento, presión, humedad, sol, etc.) para esos días lluviosos. Los valores nulos se reemplazan por 0 para evitar errores.

y_prec: la variable que queremos predecir, que es la cantidad de lluvia ese día.

3. Separar datos en entrenamiento y prueba:

X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X_prec, y_prec, test_size=0.2, random_state=42)
Se divide el dataset en un conjunto para entrenar el modelo (80%) y otro para evaluar su rendimiento (20%).

4. Entrenar el modelo de regresión lineal:

reg = LinearRegression()
reg.fit(X_train_reg, y_train_reg)
Se crea un modelo de regresión lineal y se ajusta con los datos de entrenamiento, aprendiendo una función lineal que relaciona las variables climáticas con la cantidad de lluvia.

5. Predecir la cantidad de lluvia en el conjunto de prueba:

y_pred_reg = reg.predict(X_test_reg)
El modelo genera predicciones de cuánto va a llover en los días de prueba, basándose en sus características.

6. Calcular el coeficiente de determinación R²:

r2_train = reg.score(X_train_reg, y_train_reg)
r2_test = reg.score(X_test_reg, y_test_reg)
R² (R cuadrado) indica qué tan bien el modelo explica la variabilidad de los datos.

R² = 1 significa ajuste perfecto; 0 significa que el modelo no explica nada.

Se calcula para el conjunto de entrenamiento y para el conjunto de prueba para evaluar si el modelo generaliza bien.

7. Mostrar resultados en Streamlit:

st.subheader("Resultados:")
st.markdown(f"🎯 R² entrenamiento: `{r2_train:.2f}`")
st.markdown(f"🧪 R² prueba: `{r2_test:.2f}`")
Se presentan los valores de R² para entrenamiento y prueba en la app, para que puedas ver la precisión del modelo.

# Qué representa la gráfica que se genera

Tipo de gráfico: gráfico de dispersión (scatter plot) con puntos (círculos) que representan pares de datos reales y predichos.

Eje X: cantidad real de lluvia medida en los días de prueba (y_test_reg).

Eje Y: cantidad de lluvia predicha por el modelo para esos mismos días (y_pred_reg).

Puntos: cada punto (círculo) es un día lluvioso en el conjunto de prueba. La posición horizontal es la lluvia real y la vertical la lluvia que predijo el modelo.

Línea roja punteada (r--): representa la línea ideal de ajuste perfecto, donde la predicción es igual a la realidad (y = x).
Si el modelo fuera perfecto, todos los puntos estarían justo sobre esta línea.

Concentración de puntos en la parte baja izquierda:
Eso indica que la mayoría de los días lluviosos tienen poca cantidad de lluvia (valores bajos en el eje X) y las predicciones también son bajas (valores bajos en eje Y).
Es normal que en datos de lluvia la distribución sea así, porque suele llover poco muchos días y mucho pocos días.

Puntos alejados de la línea: muestran días en los que la predicción no fue tan precisa (subestimación o sobreestimación).

Alpha=0.5: hace los puntos semitransparentes para que puedas distinguir zonas donde se superponen muchos puntos.

¿Qué puedes concluir con ese gráfico?
Si los puntos están muy dispersos y lejos de la línea roja, el modelo no predice bien.

Si están cerca y forman una nube alrededor de la línea, la predicción es buena.

La concentración baja indica que la mayoría de valores están en un rango pequeño de lluvia, lo que puede dificultar la predicción precisa para valores extremos (lluvias intensas).

