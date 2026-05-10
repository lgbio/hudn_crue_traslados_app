"""
Migración destructiva: refactoriza campos fecha/hora a DateTimeField y elimina ControlMes.

Operaciones:
1. Elimina todos los registros de TrasladoPaciente.
2. Elimina el índice sobre `fecha`.
3. Elimina los campos `fecha`, `hora_reporte`, `hora_egreso`, `hora_ingreso`.
4. Agrega `fecha_reporte`, `fecha_egreso`, `fecha_ingreso` como DateTimeField.
5. Actualiza ordering a ['-fecha_reporte'].
6. Agrega índice sobre `fecha_reporte`.
7. Elimina el modelo ControlMes.
"""

import django.utils.timezone
from django.db import migrations, models


def eliminarRegistros (apps, schema_editor):
	"""Elimina todos los registros de TrasladoPaciente antes de modificar el esquema."""
	TrasladoPaciente = apps.get_model ('traslados', 'TrasladoPaciente')
	TrasladoPaciente.objects.all ().delete ()


def noOp (apps, schema_editor):
	"""Operación inversa vacía (migración no reversible en la práctica)."""
	pass


class Migration (migrations.Migration):
	"""Migración destructiva que refactoriza campos fecha/hora y elimina ControlMes."""

	dependencies = [
		('traslados', '0002_trasladopaciente_aux_enfermeria'),
	]

	operations = [
		# 1. Eliminar todos los registros de TrasladoPaciente
		migrations.RunPython (eliminarRegistros, noOp),

		# 2. Eliminar índice sobre `fecha`
		migrations.RemoveIndex (
			model_name='trasladopaciente',
			name='traslados_t_fecha_2f751f_idx',
		),

		# 3. Eliminar campos antiguos
		migrations.RemoveField (
			model_name='trasladopaciente',
			name='fecha',
		),
		migrations.RemoveField (
			model_name='trasladopaciente',
			name='hora_reporte',
		),
		migrations.RemoveField (
			model_name='trasladopaciente',
			name='hora_egreso',
		),
		migrations.RemoveField (
			model_name='trasladopaciente',
			name='hora_ingreso',
		),

		# 4. Agregar nuevos campos DateTimeField
		migrations.AddField (
			model_name='trasladopaciente',
			name='fecha_reporte',
			field=models.DateTimeField (default=django.utils.timezone.now),
			preserve_default=False,
		),
		migrations.AddField (
			model_name='trasladopaciente',
			name='fecha_egreso',
			field=models.DateTimeField (blank=True, null=True),
		),
		migrations.AddField (
			model_name='trasladopaciente',
			name='fecha_ingreso',
			field=models.DateTimeField (blank=True, null=True),
		),

		# 5. Actualizar ordering del modelo
		migrations.AlterModelOptions (
			name='trasladopaciente',
			options={
				'ordering': ['-fecha_reporte'],
				'verbose_name': 'Traslado de Paciente',
				'verbose_name_plural': 'Traslados de Pacientes',
			},
		),

		# 6. Agregar índice sobre `fecha_reporte`
		migrations.AddIndex (
			model_name='trasladopaciente',
			index=models.Index (fields=['fecha_reporte'], name='traslados_t_fecha_r_ea944a_idx'),
		),

		# 7. Eliminar modelo ControlMes
		migrations.DeleteModel (
			name='ControlMes',
		),
	]
