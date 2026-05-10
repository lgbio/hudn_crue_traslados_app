#!/usr/bin/env python3

import re
import pandas as pd
from datetime import datetime, time
import pandas as pd
import traceback

def import_traslados_from_excel (file_path, sheet_name="ABRIL"):
	idx = 0
	skipN  = 7       # Number of lines to skip containing excel header
	try:
		# Read Excel starting at row 9	 (index 8)
		df        = pd.read_excel ( file_path, sheet_name=sheet_name, skiprows=skipN)
		print (f"+++ {len (list (df.iterrows()))=}")
		registros = []
		for idx, row in df.iterrows ():
			try:
				print (f"+++ row {idx}")
				for r in row:
					print (f"\t+++ {r=}")

				if pd.isna (row.iloc[0]):
					continue

				#fecha = pd.to_datetime (row.iloc[0]).date ()
				fechas   = parse_dates (row.iloc[0])
				fechaReporte, fechaIngreso = fechas ["reporte"], fechas ["ingreso"]
				print (f"+++ {fechaReporte=}")
				print (f"+++ {fechaIngreso=}")
				print (f"+++ {row.iloc [0]=}")
				print (f"+++ {row.iloc [1]=}")
				print (f"+++ {row.iloc [2]=}")
				print (f"+++ {row.iloc [3]=}")
				print (f"+++ {row.iloc [4]=}")

				obj = TrasladoPaciente (
					fecha_reporte=parse_datetime (fechaReporte, row.iloc[1]),
					fecha_egreso=parse_datetime (fechaReporte, row.iloc[2]),
					fecha_ingreso=parse_datetime (fechaIngreso, row.iloc[3]),
					nombre_paciente=str (row.iloc[3]).strip (),
					documento=str (row.iloc[4]).strip (),
					servicio=str (row.iloc[5]).strip (),
					quien_reporta=str (row.iloc[6]).strip (),
					destino=str (row.iloc[7]).strip (),
					procedimiento=str (row.iloc[8]).strip (),
					medico=str (row.iloc[9]).strip (),
					aux_enfermeria=str (row.iloc[10]).strip (),
					conductor=str (row.iloc[11]).strip (),
					radio_operador=str (row.iloc[12]).strip (),
					ambulancia=str (row.iloc[13]).strip (),
					observacion="" if pd.isna (row.iloc[14]) else str (row.iloc[14]).strip (),
					mes=fechas["reporte"].month,
				)
			except Exception as ex:
				print (f"+++ Error leyendo archivo excel, fila: {idx+skipN+2}, Mensaje: {str(ex)}")
				traceback.print_exc ()
				continue

			for field in obj._meta.fields:
				print(field.name, getattr(obj, field.name))
			input ()
			registros.append (obj)

		# Bulk insert (fast)
		for r in registros:
			print (f"+++ {dir (r)=}")
		TrasladoPaciente.objects.bulk_create (registros, batch_size=500)
		return len (registros)
	except Exception as ex:
		raise Exception (f"Error leyendo archivo excel, fila: {idx+skipN+2}, Error: {str(ex)}")


def parse_time (value):
	if pd.isna (value):
		return None
	if isinstance (value, datetime):
		return value.time ()
	try:
		return datetime.strptime (str (value), "%H:%M").time ()
	except:
		return None


# Return datetime from fecha (MM/DD/YYYY) and hora (HH:MM); 
# defaults to 00:00 if hora is missing, None if fecha invalid.
def parse_datetime (fecha, hora):
	# fecha is mandatory
	if pd.isna (fecha):
		return None

	try: # --- Parse date ---
		if isinstance (fecha, datetime):
			fecha_part = fecha.date ()
		else:
			fecha_part = datetime.strptime (str (fecha).strip (), "%d/%m/%Y").date ()

		# --- Parse time (default 00:00 if missing) ---
		if pd.isna (hora) or str (hora).strip () == "":
			hora_part = time (0, 0)
		else:
			hora_part = datetime.strptime (str (hora).strip (), "%H:%M").time ()

		# --- Combine ---
		return datetime.combine (fecha_part, hora_part)
	except Exception as ex:
		traceback.print_exc()
		raise Exception (f"Valores erroneos de fecha y hora: {fecha=}, {hora=}")

def parse_dates (row):
	"""
	Parse one or two dates from row.iloc[0] (DD/MM/YYYY).
	Returns (fecha_inicio, fecha_fin).
	If only one date → returns it twice.
	"""
	print (f"+++ parse_dates {row=}")
	fechas = {"reporte":None, "ingreso":None}
	input()

	if type (row) is datetime:
		value = str(row).strip()
	else:
		value = str (row)

	#if pd.isna(row.iloc[0]) or value == "":
	if pd.isna (value) or value == "":
		return fechas

	# Normalize separators: "-" or multiple spaces → single space
	value = re.sub(r"[-–]", " ", value)
	value = re.sub(r"\s+", " ", value)

	parts = value.split(" ")

	try:
		# First date
		d1 = pd.to_datetime(parts[0], dayfirst=True).date()

		# Second date (if exists)
		if len(parts) > 1:
			d2 = pd.to_datetime(parts[1], dayfirst=True).date()
		else:
			d2 = d1

		return {"reporte":d1, "ingreso":d2}
	except Exception:
		raise Exception (f"Error en fechas: {str(row)}")

#--------------------------------------------------------------------
#--------------------------------------------------------------------
import os
import django

# --- DJANGO SETUP ---
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup ()
from traslados.models import TrasladoPaciente

# --- IMPORT YOUR FUNCTION ---
#from traslados.utils import import_traslados_from_excel  # adjust path if needed

def main ():
	file_path = "traslados-abril.xlsx"	# change if needed
	sheet_name = "ABRIL"

	print ("Starting import...")

	count = import_traslados_from_excel (file_path, sheet_name)

	print (f"Import finished. {count} records inserted.")


if __name__ == "__main__":
	main ()
