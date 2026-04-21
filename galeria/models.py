""" Modelos para la aplicación de galería de proyectos fotográficos y videográficos.
Incluye modelos para proyectos, categorías y elementos multimedia asociados a cada proyecto."""

# -*- coding: utf-8 -*-
import re
# urllib para parsear URLs de videos externos (YouTube, Vimeo)
from urllib.parse import parse_qs, urlparse
# De Django importamos el módulo de modelos para definir nuestras clases de datos
from django.db import models


class Categoria(models.Model):
    """ Modelo para categorizar los proyectos (e.g. "Retratos", "Paisajes", "Cortometrajes") """
    # El nombre de la categoría, que se muestra en el sitio y se usa para generar el slug
    nombre = models.CharField(max_length=100)
    # El slug se genera automáticamente a partir del nombre para usarlo en URLs amigables
    slug = models.SlugField(unique=True)

    objects = models.Manager()  # Manager por defecto para consultas básicas

    class Meta:
        """ Configuración adicional del modelo, como el nombre plural y el orden de los objetos """
        verbose_name_plural = "categorías"

    def __str__(self) -> str:
        """ Mostrar el nombre de la categoría en el admin y otros lugares """
        return f"{self.nombre}"


class Proyecto(models.Model):
    """ Modelo principal para los proyectos en el portafolio """
    # Tipo de proyecto: fotografía o video, con opciones limitadas para mantener la consistencia
    TIPO_CHOICES = [
        ('foto', 'Fotografía'),
        ('video', 'Video'),
    ]
    # Título del proyecto, que se muestra en el sitio y se usa para generar el slug
    titulo = models.CharField(max_length=200)
    # Slug se genera automáticamente a partir del título para usarlo en URLs amigables
    slug = models.SlugField(unique=True)
    # Descripción del proyecto, que se muestra en el sitio y puede incluir detalles sobre el proceso creativo, la inspiración, etc.
    descripcion = models.TextField(blank=True)
    # Tipo de proyecto, que se muestra en el sitio y se puede usar para filtrar proyectos por tipo
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    # Categoría del proyecto, que se muestra en el sitio y se puede usar para filtrar proyectos por categoría
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='proyectos',
    )
    # Imagen de portada del proyecto, que se muestra en la lista de proyectos y en la página del proyecto
    imagen_portada = models.ImageField(upload_to='portadas/')
    # Fecha del proyecto, que se muestra en el sitio y se puede usar para ordenar proyectos
    fecha = models.DateField()
    # Indica si el proyecto está destacado, que se puede usar para mostrar proyectos destacados en la página principal
    destacado = models.BooleanField(default=False)
    # Fecha de creación del proyecto, que se establece automáticamente al crear el proyecto
    creado = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # Manager por defecto para consultas básicas

    class Meta:
        """ Ordenar descendente para mostrar los proyectos más recientes primero """
        ordering = ['-fecha']

    def __str__(self) -> str:
        """ Mostrar el título del proyecto en el admin y otros lugares """
        return f"{self.titulo}"


class MediaItem(models.Model):
    """ Modelo para los elementos multimedia asociados a un proyecto """
    # Tipo de media, con opciones para imagen, video subido o video externo (YouTube/Vimeo)
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video (archivo)'),
        ('video_url', 'Video (URL externa)'),
    ]
    # Relación con el proyecto al que pertenece este elemento multimedia,
    # con borrado en cascada para eliminar los media items si se borra el proyecto
    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name='media_items',
    )
    # Tipo de media, que se muestra en el sitio y se puede usar para filtrar media items por tipo
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    # Archivo de media, que se sube al servidor y se muestra en el sitio
    archivo = models.FileField(upload_to='media_items/', blank=True)
    # URL externa para videos de YouTube/Vimeo, que se muestra en el sitio
    url_externa = models.URLField(
        blank=True,
        help_text='URL de YouTube/Vimeo para videos externos',
    )
    # Título del elemento multimedia, que se muestra en el sitio y en el admin
    titulo = models.CharField(max_length=200, blank=True)
    # Orden del elemento multimedia, que se usa para determinar el orden de visualización
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        """Orden de elementos multimedia."""
        ordering = ['orden']
        verbose_name = "elemento multimedia"
        verbose_name_plural = "elementos multimedia"

    def __str__(self) -> str:
        """ Mostrar el título del elemento multimedia en el admin y otros lugares """
        return f"{self.titulo}" or f"Media #{self.pk}"

    # Propiedad para convertir URLs de YouTube/Vimeo a su formato embed,
    # facilitando la integración de videos externos en el sitio
    @property
    def embed_url(self) -> str :
        """Convierte URLs de YouTube/Vimeo a su formato embed."""
        # Variable para almacenar la URL final, inicialmente se asigna la URL externa proporcionada
        url = self.url_externa
        # Si no hay URL externa, devolver una cadena vacía para evitar errores en el template
        if not url:
            return ''
        # YouTube: watch?v=ID, youtu.be/ID, shorts/ID
        # Parsear la URL para extraer el hostname y la ruta,
        # lo que nos permite identificar si es un video de YouTube o Vimeo y obtener el ID del video
        parsed = urlparse(url)
        # Verificar si la URL es de YouTube (puede ser youtube.com o www.youtube.com)
        # y extraer el ID del video dependiendo del formato de la URL (watch, shorts, o youtu.be)
        if 'youtube.com' in parsed.hostname or 'www.youtube.com' in parsed.hostname:
            if 'shorts' in parsed.path:
                # Extraer el ID del video de la ruta (shorts/ID)
                video_id = parsed.path.split('/shorts/')[-1].strip('/')
            else:
                # Extraer el ID del video de la query string (watch?v=ID)
                video_id = parse_qs(parsed.query).get('v', [''])[0]
            if video_id:
                return f'https://www.youtube-nocookie.com/embed/{video_id}'
        elif 'youtu.be' in parsed.hostname:
            video_id = parsed.path.strip('/')
            if video_id:
                return f'https://www.youtube-nocookie.com/embed/{video_id}'
        elif 'vimeo.com' in parsed.hostname:
            match = re.search(r'/(\d+)', parsed.path)
            if match:
                return f'https://player.vimeo.com/video/{match.group(1)}'
        return url


class ConfigSitio(models.Model):
    """ Modelo singleton para almacenar la configuración general del sitio,
    como el nombre, subtítulo, bio y las imágenes de fondo y logo. """
    # Configuración del sitio
    nombre_sitio = models.CharField(
        max_length=200, default='Tropic Visual',
        help_text='Título que aparece en la pestaña del navegador',
    )
    # El nombre del propietario o el nombre que se muestra en la página de inicio,
    # que se puede usar para personalizar el sitio y darle un toque más humano y cercano
    nombre_propietario = models.CharField(
        max_length=200, default='Miguel Acosta',
        help_text='Nombre del dueño del portafolio',
    )
    # Un subtítulo o lema que se muestra debajo del nombre en la página de inicio,
    # que se puede usar para transmitir la esencia del portafolio y atraer a los visitantes
    subtitulo = models.CharField(
        max_length=300, blank=True,
        default='Photographer & Videomaker — Capturando momentos únicos',
        help_text='Texto debajo del nombre en la página de inicio',
    )
    # Una breve biografía o descripción que se muestra en la página "Sobre Mí",
    # que se puede usar para contar la historia del propietario, su experiencia,
    # su enfoque creativo y lo que los visitantes pueden esperar de su trabajo
    bio = models.TextField(
        blank=True,
        default='We are a creative duo specializing in photography and videography, '
                'passionate about capturing unique moments and telling stories through our lens. '
                'With a keen eye for detail and a love for visual storytelling, '
                'we strive to create compelling content that resonates with our audience.',
        help_text='Texto de la página Sobre Mí',
    )
    # Imágenes de fondo
    imagen_hero = models.ImageField(
        upload_to='sitio/', blank=True,
        help_text='Imagen de fondo del encabezado/hero',
    )
    # Imagen de fondo para la pgina inicio
    imagen_fondo = models.ImageField(
        upload_to='sitio/', blank=True,
        help_text='Imagen de fondo general de la página',
    )
    # El logo que aparece en la barra de navegación,
    # que se puede usar para reforzar la identidad visual del sitio
    # y hacerlo más memorable para los visitantes
    logo = models.ImageField(
        upload_to='sitio/', blank=True,
        help_text='Logo que aparece en la barra de navegación',
    )

    # SEO
    meta_description = models.CharField(
        max_length=160, blank=True,
        help_text='Descripción para motores de búsqueda (máx. 160 caracteres)',
    )
    meta_keywords = models.CharField(
        max_length=255, blank=True,
        help_text='Palabras clave separadas por comas (ej: fotografía, video, portafolio)',
    )

    # Redes sociales (opcionales)
    instagram = models.URLField(blank=True, help_text='URL de perfil de Instagram')
    facebook = models.URLField(blank=True, help_text='URL de perfil de Facebook')
    linkedin = models.URLField(blank=True, help_text='URL de perfil de LinkedIn')
    twitter = models.URLField(blank=True, help_text='URL de perfil de Twitter / X')
    pinterest = models.URLField(blank=True, help_text='URL de perfil de Pinterest')
    youtube = models.URLField(blank=True, help_text='URL de canal de YouTube')

    objects = models.Manager()

    class Meta:
        """ Configuración del modelo singleton, con un nombre singular y plural personalizado """
        verbose_name = "configuración del sitio"
        verbose_name_plural = "configuración del sitio"

    def __str__(self) -> str:
        """ Mostrar el nombre del sitio en el admin y otros lugares """
        return f"{self.nombre_sitio}"

    def save(self, *args, **kwargs):
        """Garantizar que solo exista una instancia."""
        self.pk = 1
        return super().save(*args, **kwargs)

    # Método de clase para cargar la configuración del sitio,
    # que devuelve la única instancia existente o la crea si no existe,
    # asegurando que siempre haya una configuración disponible para el sitio
    @classmethod
    def cargar(cls):
        """Obtener o crear la única instancia."""
        # Obtener la instancia con pk=1 o crearla si no existe,
        # lo que garantiza que siempre haya una configuración disponible para el sitio
        obj, _ = cls.objects.get_or_create(pk=1)
        # Devolver la instancia de configuración del sitio
        # para que pueda ser utilizada en los templates a través del context processor
        return obj


