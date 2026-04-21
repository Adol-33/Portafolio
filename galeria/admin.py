"""Admin de la aplicación galería."""

from django.contrib import admin
from .models import Categoria, Proyecto, MediaItem, ConfigSitio


class MediaItemInline(admin.TabularInline):
    """Inline de elementos multimedia."""
    model = MediaItem
    extra = 1


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """ Configuración del admin para el modelo de categorías, mostrando el nombre y el slug """
    list_display = ['nombre', 'slug']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    """ Configuración del admin para el modelo de proyectos, con filtros por tipo y categoría """
    list_display = ['titulo', 'tipo', 'categoria', 'fecha', 'destacado']
    list_filter = ['tipo', 'categoria', 'destacado']
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [MediaItemInline]


@admin.register(ConfigSitio)
class ConfigSitioAdmin(admin.ModelAdmin):
    """Admin para la configuración del sitio (singleton)."""

    def has_add_permission(self, request):
        """ Permitir agregar solo si no existe una instancia de ConfigSitio.
        Esto asegura que solo haya una configuración del sitio. """
        # Retorna True solo si no existe ninguna instancia de ConfigSitio,
        # lo que permite agregar una nueva configuración solo si no hay ninguna existente.
        # Si ya existe una configuración, no se permitirá agregar otra.
        # Esto garantiza que la configuración del sitio sea única (singleton).
        return not ConfigSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """ No permitir eliminar la configuración del sitio. """
        return False
