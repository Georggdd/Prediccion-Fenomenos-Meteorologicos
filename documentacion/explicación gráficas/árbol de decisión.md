# La gráfica que ves: Matriz de confusión

La matriz de confusión es una tabla que se usa para evaluar el rendimiento de un modelo de clasificación. En tu caso, el modelo clasifica si llovió (1) o no (0).

La matriz tiene esta estructura:

Predicho: No lluvia (0)	Predicho: Lluvia (1)
Real: No lluvia (0)	Verdaderos Negativos (VN)	Falsos Positivos (FP)
Real: Lluvia (1)	Falsos Negativos (FN)	Verdaderos Positivos (VP)

Cada uno de esos 4 recuadros representa:

- VN (Verdaderos Negativos): casos donde el modelo predijo que no llovió y realmente no llovió.
- FP (Falsos Positivos): casos donde el modelo predijo lluvia, pero realmente no llovió.
- FN (Falsos Negativos): casos donde el modelo predijo que no llovió, pero sí llovió.
- VP (Verdaderos Positivos): casos donde el modelo predijo lluvia y realmente llovió.

¿Qué significa la matriz en tu contexto?
El modelo usa las variables meteorológicas (tmed, tmin, tmax, etc.) para decidir si llovió o no un día.

La matriz te muestra cuántos días el modelo acertó y en cuáles se equivocó.

Por ejemplo, un número alto en VP y VN es bueno (aciertos).

Los números en FP y FN representan errores del modelo.

Los otros resultados que tienes:
🎯 Precisión en entrenamiento: 1.00 → El modelo acertó el 100% de los casos en los datos con los que fue entrenado (posible sobreajuste, es decir, se adaptó muy bien a esos datos).

🧪 Precisión en prueba: 0.84 → El modelo acertó el 84% de las veces en datos nuevos (test), lo que es bastante bueno.

Qué hace el código de la matriz de confusión:

cm = confusion_matrix(y_test, y_pred_clf)  # calcula la matriz de confusión real vs predicho
disp = ConfusionMatrixDisplay(confusion_matrix=cm)  # prepara la visualización
disp.plot(ax=ax2)  # dibuja la matriz en la figura de matplotlib
st.pyplot(fig2)  # la muestra en Streamlit
