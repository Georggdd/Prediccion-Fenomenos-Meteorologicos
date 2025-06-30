# Proceso de Limpieza de Datos Meteorológicos

En este documento se explica la preparación y limpieza de los datos meteorológicos obtenidos de AEMET para su posterior análisis y modelado predictivo. Los datos originales se reciben en formato JSON contenido en archivos .txt, con información diaria, mensuales y anuales de variables climáticas por estaciones meteorológicas.

# Descripción del Proceso
Carga de datos.
Se leen los archivos JSON con codificación latin1 para preservar los caracteres especiales propios del idioma español. Esto evita errores al cargar datos con tildes y caracteres no ASCII.

# Conversión a DataFrame
Los datos se transforman en un DataFrame de pandas, facilitando la manipulación estructurada y el análisis de las columnas.

# Limpieza y conversión de columnas numéricas
Muchas variables numéricas en los datos están en formato texto y usan coma como separador decimal. Se realiza un reemplazo de comas por puntos y se convierten estas columnas a tipo numérico (float), utilizando la función pd.to_numeric con manejo de errores para convertir valores no numéricos a NaN.

# Procesamiento de fechas
Las fechas, inicialmente en formato cadena, se convierten a objetos de fecha con pd.to_datetime, para facilitar futuras operaciones temporales y análisis de series.

# Normalización de texto en campos categóricos
Para evitar caracteres mal codificados (tildes, eñes, etc.), se aplica una normalización Unicode con unicodedata.normalize. Esto asegura la correcta representación de los caracteres en el archivo limpio y evita problemas en posteriores análisis o visualizaciones.

# Guardado del archivo limpio
El resultado se exporta a un archivo CSV con codificación utf-8-sig, que garantiza compatibilidad con herramientas comunes como Excel, manteniendo la correcta visualización de caracteres especiales.

# Técnicas y Herramientas
- Pandas para manipulación y transformación eficiente de datos tabulares.
- Codificación latin1 y utf-8-sig para manejo adecuado de caracteres especiales en la entrada y salida.
- Normalización Unicode para resolver problemas de codificación en campos de texto.
- Conversión segura a tipos numéricos con manejo de valores erróneos o faltantes.
- Conversión de fechas para facilitar análisis temporales.