import numpy as np
import re, random

def leerBase():
	'''
	Funcion que leer una base de conocimiento y la transforma en un arreglo de filas
	'''
	datos = []
	archivo = open('nombre archivo.txt', 'r')  # Reemplaza 'nombre_archivo.txt' con la ruta y nombre de tu archivo
	try:
		next(archivo)
		for linea in archivo:
			aux = linea.rstrip('\n')
			newLinea = aux.split(',')
			datos.append(newLinea)
	finally:
		archivo.close()
	return datos

def cabeceras():
	'''
	Funcion que regresa la primera columna de un archivo de conocimiento.
	'''
	archivo = open('nombre archivo.txt', 'r')  # Reemplaza 'nombre_archivo.txt' con la ruta y nombre de tu archivo
	try:
		aux = archivo.readline().rstrip('\n').split(',')
		aux = aux[1:]
	finally:
		archivo.close()
	#print(aux)
	return aux	

def obtenerDF(conocimiento):
	return 0

def obtenerIDF(df,conocimiento):
	return 0

def normalizar(conocimiento, total):
	return conocimiento

def matchUserInput(preferencia, c):
	pref = []
	for text in c:
		found = False
		for r in preferencia:
			if r.strip().lower() == text.strip().lower():
				#print("MATCH:", r)
				pref.append(1)
				found = True
				break
		if not found:
			pref.append(0)
	return pref

def matchPreference(preferencia, conocimiento):
	recomendado = ""
	'''
	Calcular el angulo minimo entre el input, y la base de conocimiento
	'''
	return recomendado