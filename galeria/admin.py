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
        return not ConfigSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
