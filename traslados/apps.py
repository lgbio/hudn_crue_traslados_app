"""
Configuración de la aplicación traslados.
"""

from django.apps import AppConfig


class AppTrasladosConfig (AppConfig):
	"""Configuración principal de la app de registro de traslados de pacientes."""

	default_auto_field = 'django.db.models.BigAutoField'
	name = 'traslados'
	verbose_name = 'Registro de Traslados'

	def ready (self):
		"""Registra señales de la app."""
		import traslados.models  # noqa: F401 — registra señales post_save
