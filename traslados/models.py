"""
Modelos de la aplicación traslados.

Define las entidades principales del sistema de registro de traslados:
Usuario y TrasladoPaciente.
"""

import datetime

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


# ─── Modelo de usuario personalizado ─────────────────────────────────────────

class Usuario (AbstractUser):
	"""Modelo de usuario del sistema, extiende AbstractUser con nombre, correo y rol."""

	ROL_CHOICES = [
		('FUNCIONARIO', 'Funcionario'),
		('DIRECTOR', 'Director'),
	]

	nombre = models.CharField (max_length=255, blank=True, default='')
	correo = models.EmailField (blank=True, default='')
	rol = models.CharField (
		max_length=20,
		choices=ROL_CHOICES,
		default='FUNCIONARIO',
	)

	class Meta:
		verbose_name = 'Usuario'
		verbose_name_plural = 'Usuarios'

	def __str__ (self):
		"""Retorna representación legible del usuario."""
		return f"{self.username} ({self.rol})"


# ─── Registro de traslado de paciente ────────────────────────────────────────

class TrasladoPaciente (models.Model):
	"""Representa un registro de servicio de traslado de paciente."""

	fecha_reporte = models.DateTimeField ()
	fecha_egreso = models.DateTimeField (null=True, blank=True)
	fecha_ingreso = models.DateTimeField (null=True, blank=True)
	nombre_paciente = models.CharField (max_length=255)
	documento = models.CharField (max_length=50)
	servicio = models.CharField (max_length=100)
	quien_reporta = models.CharField (max_length=100)
	destino = models.CharField (max_length=100)
	procedimiento = models.CharField (max_length=255)
	medico = models.CharField (max_length=100)
	aux_enfermeria = models.CharField (max_length=100, blank=True, default='')
	conductor = models.CharField (max_length=100)
	radio_operador = models.CharField (max_length=100)
	ambulancia = models.CharField (max_length=100)
	observacion = models.TextField (blank=True, default='')
	mes = models.IntegerField (editable=False)

	class Meta:
		ordering = ['-fecha_reporte']
		indexes = [
			models.Index (fields=['mes']),
			models.Index (fields=['fecha_reporte']),
		]
		verbose_name = 'Traslado de Paciente'
		verbose_name_plural = 'Traslados de Pacientes'

	def __str__ (self):
		"""Retorna representación legible del traslado."""
		return f"{self.fecha_reporte} – {self.nombre_paciente}"

	def clean (self):
		"""Valida que la fecha de reporte no sea futura."""
		if self.fecha_reporte:
			self.mes = self.fecha_reporte.month
			hoy = datetime.date.today ()
			if self.fecha_reporte.date () > hoy:
				raise ValidationError ({'fecha_reporte': 'La fecha no puede ser futura.'})

	def save (self, *args, **kwargs):
		"""Deriva el campo mes desde fecha_reporte y valida antes de persistir."""
		self.mes = self.fecha_reporte.month
		self.full_clean ()
		super ().save (*args, **kwargs)
