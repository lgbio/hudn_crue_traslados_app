# Formularios de la aplicación traslados.

import datetime

from django import forms
from django.contrib.auth import get_user_model

from .models import TrasladoPaciente

Usuario = get_user_model ()


# ─── Tailwind CSS classes reutilizables ──────────────────────────────────────

_CLASES_INPUT = (
	'w-full border border-gray-300 rounded-md px-3 py-2 text-sm '
	'focus:outline-none focus:ring-2 focus:ring-blue-500'
)


# ─── Widget personalizado fecha + hora separados ─────────────────────────────

class WidgetFechaHoraSeparados (forms.SplitDateTimeWidget):
	"""Widget que renderiza fecha y hora como dos inputs separados con estilos Tailwind."""

	def __init__ (self, attrs=None):
		"""Inicializa los sub-widgets de fecha (type=date) y hora (type=text, HH:MM)."""
		widgetsFechaHora = [
			forms.DateInput (format='%Y-%m-%d', attrs={
				'type': 'date',
				'class': _CLASES_INPUT,
			}),
			forms.TimeInput (format='%H:%M', attrs={
				'type': 'text',
				'placeholder': 'HH:MM',
				'pattern': '[0-2][0-9]:[0-5][0-9]',
				'maxlength': '5',
				'class': _CLASES_INPUT,
			}),
		]
		# Llamar al __init__ de MultiWidget directamente, pasando los sub-widgets
		forms.MultiWidget.__init__ (self, widgets=widgetsFechaHora, attrs=attrs)


# ─── Campo SplitDateTimeField que acepta hora vacía ──────────────────────────

class CampoFechaHoraOpcional (forms.SplitDateTimeField):
	"""SplitDateTimeField que retorna None cuando el componente de hora está vacío."""

	def clean (self, value):
		"""Retorna None si la hora está vacía, independientemente de la fecha."""
		# value es una lista [fecha_str, hora_str] proveniente del SplitDateTimeWidget
		if isinstance (value, (list, tuple)) and len (value) == 2:
			horaStr = value [1]
			if not horaStr or not str (horaStr).strip ():
				return None
		return super ().clean (value)


# ─── Formulario principal de traslado ────────────────────────────────────────

class FormularioTraslado (forms.ModelForm):
	"""Formulario para crear y editar registros de TrasladoPaciente."""

	# ── Campos explícitos con SplitDateTimeField + widget personalizado ───
	fecha_reporte = forms.SplitDateTimeField (
		required=True,
		widget=WidgetFechaHoraSeparados (),
		label='Fecha Reporte',
	)
	fecha_egreso = CampoFechaHoraOpcional (
		required=False,
		widget=WidgetFechaHoraSeparados (),
		label='Fecha Egreso',
	)
	fecha_ingreso = CampoFechaHoraOpcional (
		required=False,
		widget=WidgetFechaHoraSeparados (),
		label='Fecha Ingreso',
	)

	class Meta:
		model = TrasladoPaciente
		fields = [
			'fecha_reporte',
			'fecha_egreso',
			'fecha_ingreso',
			'nombre_paciente',
			'documento',
			'servicio',
			'quien_reporta',
			'destino',
			'procedimiento',
			'medico',
			'aux_enfermeria',
			'conductor',
			'radio_operador',
			'ambulancia',
			'observacion',
		]
		widgets = {
			'nombre_paciente': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 255,
				}
			),
			'documento': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 50,
				}
			),
			'servicio': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 100,
				}
			),
			'quien_reporta': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 100,
				}
			),
			'destino': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 100,
				}
			),
			'procedimiento': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 255,
				}
			),
			'medico': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 100,
				}
			),
			'aux_enfermeria': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 100,
				}
			),
			'conductor': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 100,
				}
			),
			'radio_operador': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 100,
				}
			),
			'ambulancia': forms.TextInput (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'maxlength': 100,
				}
			),
			'observacion': forms.Textarea (
				attrs={
					'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
					'rows': 3,
				}
			),
		}
		labels = {
			'fecha_reporte': 'Fecha Reporte',
			'fecha_egreso': 'Fecha Egreso',
			'fecha_ingreso': 'Fecha Ingreso',
			'nombre_paciente': 'Nombre de Paciente',
			'documento': 'Documento',
			'servicio': 'Servicio',
			'quien_reporta': 'Quien Reporta',
			'destino': 'Destino',
			'procedimiento': 'Procedimiento',
			'medico': 'Médico',
			'aux_enfermeria': 'Aux. Enfermería',
			'conductor': 'Conductor',
			'radio_operador': 'Radio Operador',
			'ambulancia': 'Ambulancia de Traslado',
			'observacion': 'Observación',
		}

	def __init__ (self, *args, **kwargs):
		"""Inicializa el formulario con valores por defecto de fecha y hora."""
		super ().__init__ (*args, **kwargs)

		# Solo precargar valores por defecto para registros nuevos (sin instancia existente)
		if self.instance is None or not self.instance.pk:
			hoyISO = datetime.date.today ().isoformat ()
			horaActual = datetime.datetime.now ().strftime ('%H:%M')

			self.initial ['fecha_reporte'] = [hoyISO, horaActual]
			self.initial ['fecha_egreso'] = [hoyISO, '']
			self.initial ['fecha_ingreso'] = [hoyISO, '']

	def clean_fecha_egreso (self):
		"""Retorna None si el componente de hora está vacío."""
		return self.cleaned_data.get ('fecha_egreso')

	def clean_fecha_ingreso (self):
		"""Retorna None si el componente de hora está vacío."""
		return self.cleaned_data.get ('fecha_ingreso')


class FormularioCrearUsuario (forms.Form):
	"""Formulario para crear un nuevo usuario con username, contraseña inicial y rol."""

	username = forms.CharField (
		label='Nombre de usuario',
		max_length=150,
		widget=forms.TextInput (attrs={
			'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
			'autocomplete': 'off',
		}),
	)
	password = forms.CharField (
		label='Contraseña inicial',
		widget=forms.PasswordInput (attrs={
			'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
			'autocomplete': 'new-password',
		}),
	)
	rol = forms.ChoiceField (
		label='Rol',
		choices=Usuario.ROL_CHOICES,
		widget=forms.Select (attrs={
			'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
		}),
	)


class FormularioCambiarContrasenaPropia (forms.Form):
	"""Formulario para que el usuario autenticado cambie su propia contraseña."""

	contrasena_actual = forms.CharField (
		label='Contraseña actual',
		widget=forms.PasswordInput (attrs={
			'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
			'autocomplete': 'current-password',
		}),
	)
	nueva_contrasena = forms.CharField (
		label='Nueva contraseña',
		widget=forms.PasswordInput (attrs={
			'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
			'autocomplete': 'new-password',
		}),
	)
	confirmar_contrasena = forms.CharField (
		label='Confirmar nueva contraseña',
		widget=forms.PasswordInput (attrs={
			'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
			'autocomplete': 'new-password',
		}),
	)

	def clean (self):
		"""Valida que la nueva contraseña y su confirmación coincidan."""
		datos = super ().clean ()
		nuevaContrasena = datos.get ('nueva_contrasena')
		confirmarContrasena = datos.get ('confirmar_contrasena')

		if nuevaContrasena and confirmarContrasena and nuevaContrasena != confirmarContrasena:
			raise forms.ValidationError ('La nueva contraseña y su confirmación no coinciden.')

		return datos


class FormularioCambiarContrasenaUsuario (forms.Form):
	"""Formulario para que el DIRECTOR cambie la contraseña de otro usuario."""

	nueva_contrasena = forms.CharField (
		label='Nueva contraseña',
		widget=forms.PasswordInput (attrs={
			'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
			'autocomplete': 'new-password',
		}),
	)
	confirmar_contrasena = forms.CharField (
		label='Confirmar contraseña',
		widget=forms.PasswordInput (attrs={
			'class': 'w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500',
			'autocomplete': 'new-password',
		}),
	)

	def clean (self):
		"""Valida que la nueva contraseña y su confirmación coincidan."""
		datos = super ().clean ()
		nuevaContrasena = datos.get ('nueva_contrasena')
		confirmarContrasena = datos.get ('confirmar_contrasena')

		if nuevaContrasena and confirmarContrasena and nuevaContrasena != confirmarContrasena:
			raise forms.ValidationError ('La nueva contraseña y su confirmación no coinciden.')

		return datos
