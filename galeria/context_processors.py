""" Context processors de la app galeria.
Inyectan la configuración del sitio en todos los templates.
"""

# import modelo de configuración del sitio
from .models import ConfigSitio


def config_sitio(_request):
    """Inyectar la configuración del sitio en todos los templates."""
    # cargar la configuración del sitio y devolverla en un diccionario
    return {'sitio': ConfigSitio.cargar()}
