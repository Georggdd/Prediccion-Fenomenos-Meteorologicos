# Comandos Git usados en el proyecto

Aquí se documentan los comandos Git usados para gestionar el repositorio.

- `git init` 
Inicializa un nuevo repositorio Git local en la carpeta actual. Crea una subcarpeta oculta llamada .git donde se guardan todos los metadatos de versiones.

- `git remote add origin <url>` 
Conecta tu repositorio local con un repositorio remoto en GitHub.
origin es el nombre que le damos a la URL remota (puede ser otro nombre, pero por convención se usa origin).

- `git branch -M main` 
Cambia el nombre de la rama principal a main (si no existía, la crea).
Antiguamente se llamaba master, pero hoy en día se recomienda usar main.

- `git add .` 
Añade todos los archivos de la carpeta al área de staging, es decir, los prepara para ser confirmados (commiteados).
El punto (.) significa "todos los archivos y subcarpetas".

- `git commit -m "mensaje"` 
Confirma (guarda) los cambios añadidos con git add, junto con un mensaje descriptivo (en este caso, "Estructura inicial del proyecto").
Los commits son como versiones guardadas del proyecto.

- `git push -u origin main` 
Sube la rama main del repositorio local al repositorio remoto (origin, en GitHub).
La opción -u establece un tracking entre tu rama local y la remota, así en el futuro solo necesitarás usar git push.

