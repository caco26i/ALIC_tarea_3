from __future__ import division								
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys
#import numpy as np
#import scipy as sp
#import scipy.linalg
import warnings
import pprint

class App4:
	cantidad_vectores_app_1 = None
	# R2, R3, o R1
	cantidad_elementos_vector_app_1 = None
	orden_matriz_app_2 = None

	matriz_elementos_app_1 = None
	orden_matrix_app_3 = None
	orden_matrix_app_4 = None

	def __init__(self):
		self.glade_file = "view.glade"
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.glade_file)
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("main_window")
		self.window.show_all()

	def on_window_destroy(self, object, data=None):
		print("quit with cancel")
		Gtk.main_quit()
		sys.exit(0)

	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def boton_app_1_siguiente_1(self, button):
		App_1 = self.builder.get_object("App_1")
		combobox_tipo_vectores = self.builder.get_object("combobox_tipo_vectores")
		combobox_tipo_vectores_value = self.get_combo_value(combobox_tipo_vectores)
		combobox_cant_vectores = self.builder.get_object("combobox_cant_vectores")
		combobox_cant_vectores_value = self.get_combo_value(combobox_cant_vectores)
		print(combobox_tipo_vectores_value)
		print(combobox_cant_vectores_value)
		tipo_operacion = ""
		if combobox_tipo_vectores_value is not None and combobox_cant_vectores_value is not None:

			if combobox_cant_vectores_value.isdigit():
				self.cantidad_vectores_app_1 = int(combobox_cant_vectores_value)
				tipo_operacion = "dependencia"
			else:
				self.cantidad_vectores_app_1 = 3
				tipo_operacion = "generado"

			if combobox_tipo_vectores_value == "R":
				self.cantidad_elementos_vector_app_1 = 1
			elif combobox_tipo_vectores_value == "R2":
				self.cantidad_elementos_vector_app_1 = 2
			elif combobox_tipo_vectores_value == "R3":
				self.cantidad_elementos_vector_app_1 = 3

			for i in range(0, 5):
				vector = self.builder.get_object("hbox_vector_"+str(i+1))
				vector_visible = i+1 <= self.cantidad_vectores_app_1
				vector.set_visible(vector_visible)
				if vector_visible:
					for j in range(0, 3):
						field_visible = j+1 <= self.cantidad_elementos_vector_app_1

						if i < 3 and j <= self.cantidad_elementos_vector_app_1: #para ocultar los campos de la ventana de pertence al generado
							field_pertenece_gen = self.builder.get_object("entry_v_"+str(i)+"_"+str(j))
							field_pertenece_gen.set_visible(field_visible)
						field = self.builder.get_object("entry_vector_"+str(i+1)+"_"+str(j+1))
						field.set_visible(field_visible)
			if tipo_operacion == "generado":
				App_1.set_current_page(2)
			else:
				App_1.set_current_page(1)

	#APP 1
	def boton_app_1_llenar_matriz(self, button):
		app_2 = self.builder.get_object("App_2")
		combobox_cant_vectores1 = self.builder.get_object("combobox_cant_vectores1")
		combobox_cant_vectores1_value = self.get_combo_value(combobox_cant_vectores1)
		print(combobox_cant_vectores1_value)
		if combobox_cant_vectores1_value is not None:
			self.orden_matriz_app_2 = combobox_cant_vectores1_value
			for i in range(0, 5):
				for j in range(0, 5):
					field = self.builder.get_object("entry_matrix_" + str(i) + "_" + str(j))
					field_visible = j < self.orden_matriz_app_2 and i < self.orden_matriz_app_2
					field.set_visible(field_visible)
			app_2.next_page()

	def calcular_LU(self, button):
		app_2 = self.builder.get_object("App_2")
		isValid = True
		matriz_elementos = []
		for i in range(0, self.orden_matriz_app_2):
			temp_list = []
			for j in range (0, self.orden_matriz_app_2):
				field = self.builder.get_object("entry_matrix_"+str(i)+"_"+str(j))
				if field.get_text().lstrip('-').isdigit():
					value_field = float(field.get_text())
					temp_list.append(value_field)
				else:
					isValid = False
					break
			if not isValid:
				break
			matriz_elementos.append(temp_list)

		label = self.builder.get_object("label_base_app_2")
		if isValid:
			try:
				P, L, U = lu_decomposition(matriz_elementos)
				label.set_text("P = \n" + formatMatrix(P) + " \n\nL = \n" + formatMatrix(L) + " \n\nU = \n" + formatMatrix(U))
			except ValueError:
				label.set_text('No tiene factorizacion LU')
		app_2.next_page()

	def open_first_page(self, button):
		notebook.set_current_page(0)

	#GETTERS AND SETTERS
	def get_combo_value(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			model = combo.get_model()
			return model[tree_iter][0]


	# App 2
	def boton_app_2_llenar_matriz(self, button):
		app_3 = self.builder.get_object("App_1")
		combobox_cant_vectores2 = self.builder.get_object("combobox_cant_vectores2")
		combobox_cant_vectores2_value = self.get_combo_value(combobox_cant_vectores2)
		print(combobox_cant_vectores2_value)
		if combobox_cant_vectores2_value is not None:
			self.orden_matriz_app_2 = combobox_cant_vectores2_value
			for i in range(0, 5):
				for j in range(0, 5):
					field = self.builder.get_object("entry_matrix2_" + str(i) + "_" + str(j) )			
					field_visible = j < self.orden_matriz_app_2 and i < self.orden_matriz_app_2
					field.set_visible(field_visible)
				field_respuesta = self.builder.get_object("entry_matrix_" + str(i) + "_r")
				field_respuesta_visible = i < self.orden_matriz_app_2
				field_respuesta.set_visible(field_respuesta_visible)

			self.metodo_app_2 = self.get_combo_value(self.builder.get_object("combobox_metodo"))
			self.max_error_app_2 = self.builder.get_object("max_error").get_text()
			self.max_iteraciones_app_2 = self.builder.get_object("max_iteraciones").get_text()

			if self.metodo_app_2 is not "" and self.max_error_app_2 is not "" and self.max_iteraciones_app_2 is not "":
				print self.metodo_app_2
				print self.max_error_app_2
				print self.max_iteraciones_app_2
				app_3.next_page()
	
	def calcular_sistema(self, button):
		app_2 = self.builder.get_object("App_1")
		isValid = True
		matriz_elementos = []		
		matriz_respuesta = []
		for i in range(0, self.orden_matriz_app_2):
			temp_list = []
			for j in range (0, self.orden_matriz_app_2):
				field = self.builder.get_object("entry_matrix2_"+str(i)+"_"+str(j))
				if field.get_text().lstrip('-').isdigit():
					value_field = float(field.get_text())
					temp_list.append(value_field)
				else:
					isValid = False
					break

			field_respuesta = self.builder.get_object("entry_matrix_" + str(i) + "_r")
			if field_respuesta.get_text().lstrip('-').isdigit():
				value_field_respuesta = float(field_respuesta.get_text())
				matriz_respuesta.append(value_field_respuesta)
			else:
				isValid = False

			if not isValid:
				break

			matriz_elementos.append(temp_list)

		label = self.builder.get_object("label_base_app_2")
		if isValid:
			if self.metodo_app_2 == "Jacobi":
				print "es Jacobi"
				self.jacobi_reg(matriz_elementos, self.max_error_app_2, self.max_iteraciones_app_2)											
			else:
				print "es Gauss-Seidel"

			print matriz_elementos			
			print matriz_respuesta
			app_2.next_page()


	##### Inicio de la funcion que aplica los metodos	######

	def jacobi_reg(self, mat, Error, MaX): 
		columnas = 0
		numIT = 1									
		switchh = False	

	##### Aplica	metodo Gauss-Jacobi ######

		filas = len(mat)															
		for C in mat[0]:
			columnas += 1																 

		print ">> Dimension de la Matriz: [%d][%d]\n" %(filas, columnas)	## Imprime numero de filas x columnas
		if ((columnas - filas) != 1):
			print ">> *** Existen mas filas	que columnas ***\n"
			sys.exit(1)

		###### Primer iteracion ######
		B = list(zip(*mat)[-1])												## B[] Vector que guarda la ultima columna de la matriz
		X0 = [B[i]/mat[i][i] for i in xrange(filas)]	## Guarda	resultado de X[i]= b1/a11 , X[i]=b2/a22 etc..
		X1 = list(X0)																	## X1(actual) = X0(anterior)

		###### Segunda iteracion ######
		numIT += 1									
		while not switchh:
			sup = 0
			div = 0

			for i in xrange(filas):
				X1[i] = B[i]
				for j in xrange(columnas-1):
					if ( i != j):
						X1[i]=	(X1[i] - (mat[i][j] * X0[j]))

				X1[i] =	(1/mat[i][i] * X1[i])
				aux = X1[i] - X0[i]
				if (aux < 0) :
					aux = aux * -1
				aux2 = X1[i]
				if (aux2 < 0):
					aux2 = aux2 * -1
				if (aux > sup):
					sup = aux
				if (aux2 > div):
					div = aux2
			X0 = list(X1)
			if (sup / div) <= Error:
				switchh = True 
				numIT += 1
			if int(numIT) > int(MaX):
				print ">> **Imposible** encontrar resultado en %s *iteraciones*.\n" % MaX	 
				sys.exit(0)
	 
		printM(mat)																			 
		my_cont = 0
		print "*** GauSS-JaCoBi ***"
		for i in X0:																		 ## Imprime	X, resultados de gauss-jacobi
			print "X%d = %f" % ((my_cont+1), i)
			my_cont += 1
		print "\n>> Numero de iteraciones: %d " % numIT
		print ">> Valor do error: %s" % Error

		####### Fin de Gauss-

		for a in xrange(1, filas):											## Checar a a triangular inferior	
			for b in xrange(0, columnas):								 
				if (int(a) != int(b)):
					if (int(mat[a][b]) != 0):
						print ">> **Imposible** calcular	triangular inferior * debe ser diferente de 0*\n" 
						sys.exit(0)
				elif (int(a) == int(b)):
						break
				
		switchh = False
		i = filas-1
		j = i 
		B[j] = B[j] / mat[i][j]
		i -= 1

		j = i
		t = 0
		numIT = 1
		columnas -= 1

		while not (switchh):
			div = 0
			numIT += 1
			for t in xrange(j+1, columnas):
				div = div + (mat[i][t] * B[t])
			B[j] = (B[j] - div) / mat[i][j]
			if int(i) == 0:
				switchh = True
			i -= 1
			j = i

		my_cont = 0
		for i in B:																 ## Imprime B, vetor que guarda resultados retornados
			print "B%d = %f" % ((my_cont+1), i)
			my_cont += 1 
	
	
warnings.filterwarnings('error')

def mult_matrix(M, N):
																																																		 
	tuple_N = zip(*N)

	# comprension de la lista anidada para calcular el producto de matrices																																													 
	return [[sum(el_m * el_n for el_m, el_n in zip(row_m, col_n)) for col_n in tuple_N] for row_m in M]

def pivot_matrix(M):
	"""Returna el pivote de la matriz	M"""
	m = len(M)

	# Crear una	matriz, identica con	valores flotantes																																															
	id_mat = [[float(i ==j) for i in range(m)] for j in range(m)]

	# Reordenar la matriz identidad de manera que el elemento mas grande de cada columna
	# de M se coloque en la diagonal de M																																															
	for j in range(m):
		row = max(range(j, m), key=lambda i: abs(M[i][j]))
		if j != row:
			# intercambiar filas																																																							
			id_mat[j], id_mat[row] = id_mat[row], id_mat[j]

	return id_mat

def lu_decomposition(A):
	"""Hacer Decomposicion LU de A (debe ser cuadrada)																																														
	 PA = LU. la funcion retorna P, L y U."""
	n = len(A)

	# crear matrices nulas para L y U																																																				 
	L = [[0.0] * n for i in range(n)]
	U = [[0.0] * n for i in range(n)]

	# Crear el pivote de la matriz P y el producto de PA																																														 
	P = pivot_matrix(A)
	PA = mult_matrix(P, A)

	# Descomposicion	LU																																																					
	for j in range(n):
		# todas las	diagonales de L son unidad																																																	 
		L[j][j] = 1.0

		for i in range(j+1):
			s1 = sum(U[k][j] * L[i][k] for k in range(i))
			U[i][j] = PA[i][j] - s1
																																								
		for i in range(j, n):
			s2 = sum(U[k][j] * L[i][k] for k in range(j))
			L[i][j] = (PA[i][j] - s2) / U[j][j]

	return (P, L, U)
	
def formatMatrix(pMatrix):
	resultado = ""
	for i in range (len(pMatrix)):
		for j in range (len(pMatrix[0])):
			resultado += str(pMatrix[i][j])
			resultado += "\t"
		resultado += "\n"
	return resultado

if __name__ == "__main__":
	main = App4()
	Gtk.main()


############# JACOBI


class InvalidSizeError(Exception):
	"""Excepcion en caso que las matrices tengan un tamnio no adecuado"""
	pass

def printM(m):																 
	
	for j in m:
		for elem in j:
			print "%3d" % elem, 
		print ""
	print ""

def readM():																	 
	
	 matriz = []																 
	 lastsize = 0																## Guarda	tamanio de la ultima fila leida 
																							 

	 print ">> Ingrese MATRIZ:	(fila	en blanco para terminar):"
	 while 1:
			r = sys.stdin.readline()								 
			if r.strip():														
				l = r.split()												 
																							 ##.. '1 2	 32 1 2' --> ['1', '2', '32', '1', '2']
				s = len(l)														 
				if lastsize and	s != lastsize:				
					raise InvalidSizeError, "As linhas devem ter todas o mesmo numero de colunas." 
				matriz.append([float(elem) for elem in l]) ## Convierte los elementos de la fila a enteros
																								 ##.. e coloca la matriz
				lastsize = s													 
			else:
				break										 
	 return matriz									
