import csv
import math
import numpy as np

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
	archivo = open('Recetas.csv', 'r')
	try:
		aux = archivo.readline().rstrip('\n').split(',')
		aux = aux[1:]
	finally:
		archivo.close()
	return aux

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

def crearVectorUsuario():
	cabecera = cabeceras()

	proteinasReceta = crearMensaje( cabecera[:6], 0, 6 )
	metodosCoccion = crearMensaje( cabecera[6:9], 6, 9 )
	tiposReceta = crearMensaje( cabecera[9:12], 9, 12 )
	utensilios =  crearMensaje( cabecera[12:17], 12, 17 )
	complemento = crearMensaje( cabecera [17:], 17, 24 )
	
	vectorUsuario = [0] * (len(cabecera))

	validacion = 0
	while (validacion < 5):
		try:
			if validacion == 0:
				opcionEleguida = validarOpcion(proteinasReceta, 0, 6)
				vectorUsuario[opcionEleguida] = 1
			if validacion == 1:
				opcionEleguida = validarOpcion(metodosCoccion, 6, 9)
				vectorUsuario[opcionEleguida] = 1
			if validacion == 2:
				opcionEleguida = validarOpcion(tiposReceta, 9, 12)
				vectorUsuario[opcionEleguida] = 1
			if validacion == 3:
				opcionEleguida = validarOpcion(utensilios, 12, 17)
				vectorUsuario[opcionEleguida] = 1
			if validacion == 4:
				opcionEleguida = validarOpcion(complemento, 17, 24)
				vectorUsuario[opcionEleguida] = 1
			validacion+=1
		except ValueError:
			print('Ingresa un número entero')
	return vectorUsuario

def vectorPreferencia():
	vectorPreferencia = []
	recetas = obtenerRecetas()
	for receta in recetas:
		try:
			mensaje = f'Que tanto prefieres la siguiente receta: {receta}\n 1:Me gusta\n 0:Me es indiferente\n -1:No me gusta\n'
			vectorPreferencia.append(validarOpcion(mensaje, -1, 1))
		except ValueError:
			print('Ingresa un número entero')

	return vectorPreferencia

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

def columnas(conocimiento):
	'''
	Regresa las columnas de la base de conocimiento.
	'''
	columnas = []
	for columna in range(len(conocimiento[0]) - 1):
		columnas.append([renglon[columna] for renglon in conocimiento])
	return columnas

def perfilUsuario(vectorUsuario, columnas):
	return [np.dot(columna, vectorUsuario) for columna in columnas]
	

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

def prediccion(filaNormalizada, perfilUsuario, idf):
	primerProducto = np.dot(filaNormalizada, perfilUsuario)
	segundoProducto = np.dot(primerProducto, idf)
	return sum(segundoProducto)

def main():
	datos = leerBase()
	recetas = obtenerRecetas()

	print('--------------------- Atributos-------------------------')
	datosInt = totalAtributos(datos)
	#print(datosInt)	

	print('--------------------- Base normalizada ------------------------')
	normalizado = normalizar(datosInt)
	#print(normalizado)

	print('--------------------- Suma de las columnas (DF) -----------------------')
	df = (obtenerDF(datosInt))
	#print(df)

	print('--------------------- IDF -----------------------')
	longitud = len(normalizado)
	idf = obtenerIDF(df, longitud)
	#print(idf)

	print('--------------------- Perfil Usuario -------------------------')
	vectorUsuario = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
	perfil = perfilUsuario(vectorUsuario, columnas(datosInt))
	print(perfil)

	print('--------------------- Predicciones -----------------------')
	predicciones = []
	for fila in normalizado:
		predicciones.append(prediccion(fila, perfil, idf))
	print('Te recomendamos : ' + recetas[np.argmax(predicciones)])
if __name__ == "__main__":
    main()