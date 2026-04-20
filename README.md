# Portafolio

Sitio web de portafolio personal construido con Django, diseñado para mostrar proyectos fotográficos y videográficos.

## Tecnologías

- **Backend:** Django 6.0, Django REST Framework
- **Frontend:** HTML, CSS (Raleway), HTMX, Font Awesome
- **Base de datos:** SQLite

## Estructura del proyecto

```
portafolio/        # Configuración principal de Django (settings, urls, wsgi)
galeria/           # App principal: modelos, vistas, URLs y context processors
templates/         # Plantillas HTML (base, inicio, proyectos, sobre mí, contacto)
static/css/        # Estilos del sitio
media/             # Archivos subidos (imágenes, portadas)
```

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd Portafolio
   ```

2. Crear y activar el entorno virtual:
   ```bash
   python -m venv entorno/virtual
   # Windows
   entorno\virtual\Scripts\activate
   # Linux/Mac
   source entorno/virtual/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install django djangorestframework django-htmx pillow
   ```

4. Crear el archivo `secrets.json` en la raíz del proyecto:
   ```json
   {
       "SECRET_KEY": "tu-clave-secreta",
       "DEBUG": true,
       "ALLOWED_HOSTS": []
   }
   ```

5. Aplicar migraciones e iniciar el servidor:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Configuración del sitio

El contenido del sitio (nombre, logo, redes sociales, etc.) se gestiona desde el panel de administración de Django en `/admin/`, a través del modelo **ConfigSitio**.
