from __future__ import division								
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import sys
import warnings
import pprint
import numpy as np
import scipy as sp
import scipy.linalg 

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
				P, L, U = sp.linalg.lu(sp.array(matriz_elementos))
				label.set_text("P = \n" + str(P) + " \n\nL = \n" + str(L) + " \n\nU = \n" + str(U))
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
				print (self.metodo_app_2)
				print (self.max_error_app_2)
				print (self.max_iteraciones_app_2)
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
				try:
					res = jacobi(np.array(matriz_elementos), np.array(matriz_respuesta), int(self.max_iteraciones_app_2), float(self.max_error_app_2))
					print (res)
				except:
					print("El sistema no tiene solucion")
			else:
				print ("es Gauss-Seidel")
			app_2.next_page()

	
warnings.filterwarnings('error')

###Jacobi

def jacobi(A, b, iterationLimit, error):
	
	resultado = ""

	# prints the system
	resultado += "System:\n"
	for i in range(A.shape[0]):
			row = ["{}*x{}".format(A[i, j], j + 1) for j in range(A.shape[1])]
			resultado += " + " + str(row) + "=" + str(b[i]) + "\n"

	x = np.zeros_like(b)
	for it_count in range(iterationLimit):
			resultado += "\n\nSolucion actual:" + str(x) + "\n"
			x_new = np.zeros_like(x)

			for i in range(A.shape[0]):
					s1 = np.dot(A[i, :i], x[:i])
					s2 = np.dot(A[i, i + 1:], x[i + 1:])
					x_new[i] = (b[i] - s1 - s2) / A[i, i]

			if np.allclose(x, x_new, atol=error):
					break

			x = x_new

			error = np.dot(A, x) - b
			resultado += "Error:" + str(error) + "\n"

	resultado += "\n\nSolucion final:" + str(x) + "\n"

	return resultado


if __name__ == "__main__":
	main = App4()
	Gtk.main()
