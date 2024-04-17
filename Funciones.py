import numpy as np
import re, random

def leerBase():
	'''
	Funcion que leer una base de conocimiento y la transforma en un arreglo de filas
	'''
	datos = []
	archivo = open('Recetas.csv', 'r') 
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
	archivo = open('Recetas.txt', 'r')
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
	'''
	Calcular el angulo minimo entre el input, y la base de conocimiento
	'''
	indice_recomendacion = 0
	tmp = 100

	for indice,line in enumerate(conocimiento):
		distancia = np.linalg.norm(np.array(line[1::],dtype=int) - preferencia)
		print(line[0] + ': ' + str(distancia))
		if distancia <= tmp:
			tmp = distancia
			indice_recomendacion = indice
	
	recomendado = conocimiento[indice_recomendacion][0]
	return recomendado

#vector_usuario = np.array([0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,0,0,1,1,1,0,0,0,0])
# conocimiento = leerBase()
# print('Te recomendamos: ' + matchPreference(vector_usuario, conocimiento))