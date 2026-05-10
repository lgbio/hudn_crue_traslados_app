"""Servicio de generación de reportes Excel para traslados de pacientes."""

import io

import openpyxl


# Encabezados en español en el orden definido por el modelo TrasladoPaciente
ENCABEZADOS = [
	'FECHA REPORTE',
	'FECHA EGRESO',
	'FECHA INGRESO',
	'NOMBRE DE PACIENTE',
	'DOCUMENTO',
	'SERVICIO',
	'QUIEN REPORTA',
	'DESTINO',
	'PROCEDIMIENTO',
	'MÉDICO',
	'AUX. ENFERMERÍA',
	'CONDUCTOR',
	'RADIO OPERADOR',
	'AMBULANCIA DE TRASLADO',
	'OBSERVACIÓN',
]


def generarExcel (queryset, mes):
	"""Genera un archivo Excel con los registros del queryset dado.

	Crea un libro de trabajo con una hoja única que contiene los encabezados
	en español y una fila por cada registro de TrasladoPaciente. Si el queryset
	está vacío, retorna el archivo con solo los encabezados.

	Args:
		queryset: QuerySet de TrasladoPaciente con los registros a incluir.
		mes: Número de mes (1–12) usado para nombrar el archivo.

	Returns:
		tuple: (bytes del archivo .xlsx, nombre del archivo str)
	"""
	libro = openpyxl.Workbook ()
	hoja = libro.active
	hoja.title = f'Traslados Mes {mes}'

	# Escribir encabezados
	hoja.append (ENCABEZADOS)

	# Escribir una fila por registro
	for registro in queryset:
		# Eliminar tzinfo para compatibilidad con openpyxl (Excel no soporta timezones)
		fechaReporte = registro.fecha_reporte.replace (tzinfo=None) if registro.fecha_reporte else ''
		fechaEgreso = registro.fecha_egreso.replace (tzinfo=None) if registro.fecha_egreso else ''
		fechaIngreso = registro.fecha_ingreso.replace (tzinfo=None) if registro.fecha_ingreso else ''
		fila = [
			fechaReporte,
			fechaEgreso,
			fechaIngreso,
			registro.nombre_paciente,
			registro.documento,
			registro.servicio,
			registro.quien_reporta,
			registro.destino,
			registro.procedimiento,
			registro.medico,
			registro.aux_enfermeria,
			registro.conductor,
			registro.radio_operador,
			registro.ambulancia,
			registro.observacion,
		]
		hoja.append (fila)

	# Serializar a bytes en memoria
	buffer = io.BytesIO ()
	libro.save (buffer)
	buffer.seek (0)

	nombreArchivo = f'traslados_{mes}.xlsx'
	return buffer.getvalue (), nombreArchivo
