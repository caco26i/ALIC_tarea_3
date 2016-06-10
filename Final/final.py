import gi
import sys
from gi.repository import Gtk
import numpy as np
import scipy as sp
import scipy.linalg
import warnings
import pprint
gi.require_version('Gtk', '3.0')


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

    #APP 2

    def boton_app_2_llenar_matriz(self, button):
        app_2 = self.builder.get_object("App_2")
        combobox_cant_vectores1 = self.builder.get_object("combobox_cant_vectores1")
        combobox_cant_vectores1_value = self.get_combo_value(combobox_cant_vectores1)
        print(combobox_cant_vectores1_value)
        if combobox_cant_vectores1_value is not None:
            print("Entro al if")
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


    # App 3

warnings.filterwarnings('error')

if __name__ == "__main__":
    main = App4()
    Gtk.main()
