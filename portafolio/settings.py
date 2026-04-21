""" Settings de Django para el proyecto de portafolio.
"""

from pathlib import Path
import os
import json

# dj_database_url es una librería que permite configurar la base de datos desde una URL
import dj_database_url
# import whitenoise

# .env es un archivo de texto que contiene variables de entorno en formato clave=valor
from dotenv import load_dotenv

# carga las variables de entorno desde el archivo .env
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# función para obtener las variables secretas desde el archivo secrets.json
def get_secret(key, default=None) -> str:
    """Get the secret variable or return explicit exception."""
    try:
        with open((BASE_DIR / 'secrets.json'), encoding='utf-8') as f:
            secrets = json.loads(f.read())
            return secrets[key]
    except FileNotFoundError:
        return default


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", get_secret("SECRET_KEY"))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# en producción, debes configurar ALLOWED_HOSTS con los dominios de tu sitio
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.tropicvisual.com', 'tropicvisual.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic', # para usar WhiteNoise durante el desarrollo
    'galeria', # nuestra app principal
    'django_htmx', # para usar HTMX en nuestras plantillas
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portafolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'galeria.context_processors.config_sitio',
            ],
        },
    },
]

WSGI_APPLICATION = 'portafolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default = os.getenv('DATABASE_URL'))

}



# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

# archivos estáticos (CSS, JS, imágenes de la app)
STATIC_URL = '/static/'
# directorio donde Django buscará los archivos estáticos durante el desarrollo
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
# directorio donde Django recopilará los archivos estáticos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# configuración para servir archivos estáticos con WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'




# archivos multimedia (subidos por el usuario)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# configuraciones de seguridad para producción
CSRF_TRUSTED_ORIGINS = ['https://www.tropicvisual.com', 'https://tropicvisual.com']


