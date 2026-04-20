"""Context processors de la app galeria."""

from .models import ConfigSitio


def config_sitio(_request):
    """Inyectar la configuración del sitio en todos los templates."""
    return {'sitio': ConfigSitio.cargar()}
