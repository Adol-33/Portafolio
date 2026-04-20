""" Modelos para la aplicación de galería de proyectos fotográficos y videográficos.
Incluye modelos para proyectos, categorías y elementos multimedia asociados a cada proyecto."""

import re
from urllib.parse import parse_qs, urlparse

from django.db import models


class Categoria(models.Model):
    """ Modelo para categorizar los proyectos (e.g. "Retratos", "Paisajes", "Cortometrajes") """
    nombre = models.CharField(max_length=100)
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
    TIPO_CHOICES = [
        ('foto', 'Fotografía'),
        ('video', 'Video'),
    ]
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='proyectos',
    )
    imagen_portada = models.ImageField(upload_to='portadas/')
    fecha = models.DateField()
    destacado = models.BooleanField(default=False)
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
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video (archivo)'),
        ('video_url', 'Video (URL externa)'),
    ]
    proyecto = models.ForeignKey(
        Proyecto, on_delete=models.CASCADE, related_name='media_items',
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='media_items/', blank=True)
    url_externa = models.URLField(
        blank=True,
        help_text='URL de YouTube/Vimeo para videos externos',
    )
    titulo = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        """Orden de elementos multimedia."""
        ordering = ['orden']
        verbose_name = "elemento multimedia"
        verbose_name_plural = "elementos multimedia"

    def __str__(self) -> str:
        """ Mostrar el título del elemento multimedia en el admin y otros lugares """
        return f"{self.titulo}" or f"Media #{self.pk}"

    @property
    def embed_url(self):
        """Convierte URLs de YouTube/Vimeo a su formato embed."""
        url = self.url_externa
        if not url:
            return ''
        # YouTube: watch?v=ID, youtu.be/ID, shorts/ID
        parsed = urlparse(url)
        if 'youtube.com' in parsed.hostname or 'www.youtube.com' in parsed.hostname:
            if 'shorts' in parsed.path:
                video_id = parsed.path.split('/shorts/')[-1].strip('/')
            else:
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
    nombre_sitio = models.CharField(
        max_length=200, default='Tropic Visual',
        help_text='Título que aparece en la pestaña del navegador',
    )
    nombre_propietario = models.CharField(
        max_length=200, default='Miguel Acosta',
        help_text='Nombre del dueño del portafolio',
    )
    subtitulo = models.CharField(
        max_length=300, blank=True,
        default='Photographer & Videomaker — Capturando momentos únicos',
        help_text='Texto debajo del nombre en la página de inicio',
    )
    bio = models.TextField(
        blank=True,
        default='We are a creative duo specializing in photography and videography, '
                'passionate about capturing unique moments and telling stories through our lens. '
                'With a keen eye for detail and a love for visual storytelling, '
                'we strive to create compelling content that resonates with our audience.',
        help_text='Texto de la página Sobre Mí',
    )
    imagen_hero = models.ImageField(
        upload_to='sitio/', blank=True,
        help_text='Imagen de fondo del encabezado/hero',
    )
    imagen_fondo = models.ImageField(
        upload_to='sitio/', blank=True,
        help_text='Imagen de fondo general de la página',
    )
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
        return f"{self.nombre_sitio}"

    def save(self, *args, **kwargs):
        """Garantizar que solo exista una instancia."""
        self.pk = 1
        return super().save(*args, **kwargs)

    @classmethod
    def cargar(cls):
        """Obtener o crear la única instancia."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# Create your models here.
