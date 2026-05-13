"""
Configuración principal del proyecto Django — Sistema de Registro de Traslados.

Este archivo es un settings mínimo de desarrollo para ejecutar la app crue_traslados
de forma standalone para pruebas. En producción, la app principal define sus propios settings.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env (si existe)
load_dotenv (BASE_DIR / '.env')

# Clave secreta (cambiar en producción)
SECRET_KEY = 'django-insecure-cambiar-en-produccion-clave-secreta-unica'

# Modo de depuración (desactivar en producción)
DEBUG = True

ALLOWED_HOSTS = ['*']

# ─── Aplicaciones instaladas ────────────────────────────────────────────────

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'crue_traslados',
]

# ─── Middleware ──────────────────────────────────────────────────────────────

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# ─── Plantillas ─────────────────────────────────────────────────────────────

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'config.wsgi.application'

# ─── Base de datos ───────────────────────────────────────────────────────────

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get ('DB_NAME', 'traslados_db'),
		'USER': os.environ.get ('DB_USER', 'postgres'),
		'PASSWORD': os.environ.get ('DB_PASSWORD', ''),
		'HOST': os.environ.get ('DB_HOST', '127.0.0.1'),
		'PORT': os.environ.get ('DB_PORT', '5432'),
	}
}

# ─── Validación de contraseñas ───────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
	{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
	{'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
	{'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internacionalización ────────────────────────────────────────────────────

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ─── Archivos estáticos ──────────────────────────────────────────────────────

STATIC_URL       = '/static/'
STATIC_ROOT      = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = []

# ─── Archivos de medios ──────────────────────────────────────────────────────

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── Clave primaria por defecto ──────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── Autenticación ───────────────────────────────────────────────────────────

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/crue-traslados/'
LOGOUT_REDIRECT_URL = '/login/'

# ─── Hasher rápido para pruebas ──────────────────────────────────────────────

import sys
if 'test' in sys.argv or 'pytest' in sys.modules:
	PASSWORD_HASHERS = [
		'django.contrib.auth.hashers.MD5PasswordHasher',
	]
