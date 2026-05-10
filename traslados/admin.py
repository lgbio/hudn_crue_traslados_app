# Registro de modelos en el panel de administración de Django.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TrasladoPaciente, Usuario


class AdminUsuario (UserAdmin):
	"""Configuración del panel de administración para el modelo Usuario."""

	list_display = ['username', 'nombre', 'correo', 'rol', 'is_active']
	list_filter = ['rol', 'is_active']
	search_fields = ['username', 'nombre', 'correo']

	fieldsets = UserAdmin.fieldsets + (
		('Datos adicionales', {'fields': ('nombre', 'correo', 'rol')}),
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		('Datos adicionales', {'fields': ('nombre', 'correo', 'rol')}),
	)


class AdminTrasladoPaciente (admin.ModelAdmin):
	"""Configuración del panel de administración para el modelo TrasladoPaciente."""

	list_display = [
		'fecha_reporte',
		'nombre_paciente',
		'documento',
		'servicio',
		'destino',
		'aux_enfermeria',
		'conductor',
		'ambulancia',
	]
	list_filter = ['servicio', 'destino']
	search_fields = ['nombre_paciente', 'documento', 'conductor']
	ordering = ['-fecha_reporte']


admin.site.register (Usuario, AdminUsuario)
admin.site.register (TrasladoPaciente, AdminTrasladoPaciente)
