import csv
import math
import numpy as np
import random

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


def obtenerRecetas():
	recetas = []
	with open('Recetas.csv', newline='') as recetasCsv:
		filas = csv.reader(recetasCsv)
		for fila in filas:
			recetas.append(fila[0])
	recetas.pop(0)
	return recetas

def crearMensaje(opciones, inicio, fin):
	mensaje = 'Cual de las siguientes opciones prefieres: \n'

	for opcion in opciones:
		if inicio == fin - 1:
			mensaje += f'{inicio}:{opcion}.\n'
		else:
			mensaje += f'{inicio}:{opcion}, '
		inicio += 1
	return mensaje

def validarOpcion(mensaje, minimo, maximo):
	while True:
		try:
			opcion = int(input(mensaje))
			if minimo <= opcion <= maximo:
				return opcion
			else:
				print(f'El número debe estar entre {minimo} y {maximo}.')
		except ValueError:
			print('Ingresa un número entero.')



def obtenerDF(conocimiento):
	'''
	Suma los valores de cada atributo de la base de conocimiento
	'''
	columnas = []
	for columna in range(len(conocimiento[0]) - 1):
		suma = 0
		for renglon in conocimiento:
			suma += renglon[columna]
		columnas.append(suma)
	return columnas

def obtenerIDF(df,longitud):
	return [math.log(longitud/item) for item in df]

def totalAtributos(conocimiento):
	'''
	Suma los atributos presentes en cada receta y lo agrega al final de la lista
	'''
	conocimientoTotal = []
	for line in conocimiento:
		atributos = [int(atributo) for atributo in line[1:]]
		atributos.append(sum(atributos))
		conocimientoTotal.append(atributos)
	return conocimientoTotal

def normaliza(renglon, total):
	'''
	Normaliza los valores de un renglon de la base de conocimiento.
	'''
	raiz = math.sqrt(total)
	return [valor / raiz for valor in renglon]

def normalizar(conocimiento):
	'''
	Normaliza todos los renglones de la base de conocimiento.
	'''
	normalizado = []
	[normalizado.append(normaliza(linea[:-1], linea[-1])) for linea in conocimiento]
	return normalizado



def preferenciasUsuario(recetas):
    preferencias = np.zeros(len(recetas))
    indices = random.sample(range(len(recetas)), 10)
    for indice in indices:
        receta = recetas[indice]
        preferencia = input(f"¿Te gusta la receta {receta}? Responde con 1 si te gusta, -1 si no te gusta, 0 si no te importa: ")
        preferencias[indice] = int(preferencia)
    return preferencias

def columnas(conocimiento):
	'''
	Regresa las columnas de la base de conocimiento.
	'''
	columnas = []
	for columna in range(len(conocimiento[0]) - 1):
		columnas.append([renglon[columna] for renglon in conocimiento])
	return columnas

def perfilUsuario(vectorUsuario, columnas):
	'''
	Genera el perfil del usuario.
	'''
	return [np.dot(columna, vectorUsuario) for columna in columnas]


def preferenciasUsuario(recetas):
	'''
	Pregunta la opinión de 10 recetas aleatorias al usuario
	Se puede modificar la cantidad de recetas a preguntar
	'''
	preferencias = np.zeros(len(recetas))
	indices = random.sample(range(len(recetas)), 10)
	for indice in indices:
		receta = recetas[indice]
		preferencia = input(f"¿Te gusta la receta {receta}? Responde con 1 si te gusta, -1 si no te gusta, 0 si no te importa: ")
		while preferencia not in ['1', '-1', '0']:
			print("Respuesta inválida. Por favor, responde con 1, -1 o 0.")
			preferencia = input(f"¿Te gusta la receta {receta}? Responde con 1 si te gusta, -1 si no te gusta, 0 si no te importa: ")
		preferencias[indice] = int(preferencia)
	return preferencias

def prediccion(filaNormalizada, perfilUsuario, idf):
	'''
	Genera las predicciones de las recetas
	'''
	primerProducto = np.dot(filaNormalizada, perfilUsuario)
	segundoProducto = np.dot(primerProducto, idf)
	return sum(segundoProducto)

def main():
	datos = leerBase()
	recetas = obtenerRecetas()
	datosInt = totalAtributos(datos)
	normalizado = normalizar(datosInt)
	df = (obtenerDF(datosInt))
	longitud = len(normalizado)
	idf = obtenerIDF(df, longitud)
	vectorUsuario = preferenciasUsuario(recetas)
	perfil = perfilUsuario(vectorUsuario, columnas(datosInt))
	predicciones = []
	for fila in normalizado:
		predicciones.append(prediccion(fila, perfil, idf))
	print('Te recomendamos : ' + recetas[np.argmax(predicciones)])
if __name__ == "__main__":
    main()