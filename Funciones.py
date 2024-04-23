import numpy as np
import math

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

def obtenerIDF(df,conocimiento):
	return 0

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

def productoPunto(vectorUsuario, columnas):
	return [np.dot(vectorUsuario, columna) for columna in columnas]
	

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
		#print(line[0] + ': ' + str(distancia))
		if distancia <= tmp:
			tmp = distancia
			indice_recomendacion = indice
	
	recomendado = conocimiento[indice_recomendacion][0]
	return recomendado

def main():
	datos = leerBase()
	print(datos)

	# print('--------------------------------------------')

	# datosInt = totalAtributos(datos)
	# print(datosInt)	

	# print('--------------------------------------------')

	# normalizado = normalizar(datosInt)
	# print(normalizado)

	# print('--------------------------------------------')

	# print(obtenerDF(datosInt))

	# print('--------------------------------------------')
	
	# print(columnas(datosInt))

	# print('--------------------------------------------')
	# vectorUsuario = [0, 1, 0, -1, 0, 0, 1, -1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, -1]
	# print(productoPunto(vectorUsuario, columnas(datosInt)))
	

if __name__ == "__main__":
    main()