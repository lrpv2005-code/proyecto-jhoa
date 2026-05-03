# Proyecto Jhoa


## 1. Clonar el repositorio

Para descargar el proyecto en tu computadora, abre una terminal en la carpeta donde deseas guardarlo y ejecuta:

```bash
git clone https://github.com/lrpv2005-code/proyecto-jhoa.git
```

## 2. Iniciar el Servidor Web

Para arrancar el proyecto localmente y probarlo, asegúrate de estar dentro de la carpeta que contiene el archivo `manage.py` y ejecuta:

```bash
python manage.py runserver
```

Direccion de la pagina: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


## 3. Cómo Subir Cambios (Commits) a GitHub

Cuando realices modificaciones en tu código y quieras actualizar tu repositorio en GitHub, sigue estos tres pasos desde tu terminal (asegúrate de estar en la raíz de tu proyecto):

1. **Añade todos los archivos modificados:**
   ```bash
   git add .
   ```
2. **Crea un "commit" con una descripción breve de lo que hiciste:**
   ```bash
   git commit -m "Describe los cambios aquí (ej. se agregó la nueva página de inicio)"
   ```
3. **Sube los cambios a la rama principal del repositorio:**
   ```bash
   git push origin main
   ```
