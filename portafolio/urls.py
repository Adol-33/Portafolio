""" Endpoints de la aplicación portafolio """

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importar settings para configurar la ruta de archivos multimedia
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('galeria.urls')),
]

# Agregar esta línea para servir archivos multimedia durante el desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
